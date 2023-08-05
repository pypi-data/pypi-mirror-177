# 2018 to present - Copyright Microchip Technology Inc. and its subsidiaries.
#
# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.

# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR
# PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL,
# PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY
# KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP
# HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
# FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
# ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
# THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.

import os
import re
import asn1crypto
import cryptoauthlib as cal
from pathlib import Path
from .cert_utils import get_ca_status, get_device_sn_cert
from cryptography import x509
from .x509_find_elements import (
    tbs_location, public_key_location,
    signature_location, validity_location,
    name_search_location, sn_location,
    auth_key_id_location, subj_key_id_location,
    name_search_location_last)
from ctypes import (
    cast, c_uint8, POINTER, string_at,
    pointer, create_string_buffer)
from cryptography.hazmat.primitives import serialization
import _pickle


class CertDef():
    def __init__(self, device_name=''):
        self.set_cert = False
        self.device_name = device_name
        pass

    def set_certificate(self, cert, ca_cert, template_id=0):
        """
        Sets a certificate along with its CA to be processed for definition
        files.
        """
        self.cert = cert
        self.ca_cert = ca_cert
        self.template_id = template_id
        self.chain_id = 0
        if get_ca_status(cert):
            self.chain_level = 1
            self.serial_num = None
            self.ca_cert_def = None
            self.signer_id = self.__get_signer_id(cert)
            self.cert_def_name = 'signer'
            self.ca_include_filename = None
            self.ca_cert_def_var_name = None
            self.filename_base = \
                f'cust_def_{self.cert_def_name}'
        else:
            self.chain_level = 0
            find_value = '9618' if self.device_name == 'ECC204' else '0123'
            self.serial_num = get_device_sn_cert(cert, find_value)
            self.ca_cert_def = self.__get_signer_template(ca_cert)
            self.signer_id = self.__get_signer_id(ca_cert)
            self.cert_def_name = 'device'
            self.ca_include_filename = 'cust_def_signer.h'
            self.ca_cert_def_var_name = 'g_cert_def_1_signer'
            self.filename_base = \
                f'cust_def_{self.cert_def_name}'

        self.cert_def = None
        self.cert_files = None
        self.set_cert = True

    def get_py_definition(self, src_def_file='', dest_def_file=''):
        """
        Returns the certificate definition and optionally saves to file
        """
        if src_def_file and os.path.exists(src_def_file):
            with open(src_def_file, "rb") as fp:
                definition = _pickle.load(fp)
            if definition is not None and \
                    'params' in definition and \
                    'elements' in definition and \
                    'template_data' in definition:
                params = definition.get('params')
                elements = definition.get('elements')
                template_data = definition.get('template_data')
                cert_def = self.__params_atcacert_definitions(
                    template_data, params, elements)
            else:
                raise ValueError('Invalid certificate definition file')
        elif self.set_cert:
            cert_def = self.__build_py_definition()
            self.cert_def = cert_def

        if self.set_cert and dest_def_file:
            cert = dict()
            params = self.get_cert_params()
            params.update({'ca_cert_def': None})
            cert.update({
                'template_data':
                    self.cert.public_bytes(encoding=serialization.Encoding.DER)
                })
            cert.update({
                'elements':
                    self.get_cert_elements()
                })
            cert.update({'params': params})
            Path(dest_def_file).write_bytes(_pickle.dumps(cert))

        return cert_def

    def get_c_definition(self, save_files=False):
        """
        Returns the certificate C definitions and optionally saves to file
        """
        if self.set_cert:
            self.cert_def = self.__build_py_definition()
            self.cert_files = self.__build_c_definition()

            if save_files:
                for file_name, file_data in self.cert_files.items():
                    Path(file_name).write_bytes(file_data)

            return self.cert_files

    def __build_py_definition(self):
        """
        Function to build and return the certificate definition
        """
        template_data = self.cert.public_bytes(
                                    encoding=serialization.Encoding.DER)
        params = self.get_cert_params()
        elements = self.get_cert_elements()
        return self.__params_atcacert_definitions(
                                    template_data, params, elements)

    def __build_c_definition(self):
        """
        Function to build and return the C certificate definition
        """
        template_var_name = f'g_template_{self.cert_def.template_id}_{self.cert_def_name}'
        pk_var_name = f'g_cert_ca_public_key_{self.cert_def.template_id}_{self.cert_def_name}'
        elements_var_name = f'g_cert_elements_{self.cert_def.template_id}_{self.cert_def_name}'
        cert_def_var_name = f'g_cert_def_{self.cert_def.template_id}_{self.cert_def_name}'

        c_file = ''
        c_file += '#include "atcacert/atcacert_def.h"\n'
        if self.ca_include_filename:
            c_file += f'#include "{self.ca_include_filename}"\n'
        c_file += '\n'

        template_data = string_at(
                        self.cert_def.cert_template,
                        self.cert_def.cert_template_size)
        c_file += f'const uint8_t {template_var_name}[{len(template_data)}] = {self.__c_hex_array(template_data)};\n'
        c_file += '\n'

        if self.chain_level == 1:
            pk_data = self.ca_cert.public_key().public_bytes(
                format=serialization.PublicFormat.UncompressedPoint,
                encoding=serialization.Encoding.X962
            )[1:]
            c_file += f'const uint8_t {pk_var_name}[{len(pk_data)}] = \
                    {self.__c_hex_array(pk_data)};\n'
            c_file += '\n'

        if self.cert_def.cert_elements_count:
            element_strs = []
            for i in range(self.cert_def.cert_elements_count):
                element = self.cert_def.cert_elements[i]
                element_str = ''
                element_str += f'    {{\n'
                element_str += f'        .id = "{element.id if isinstance(element.id, str) else element.id.decode("ascii")}",\n'
                element_str += f'        .device_loc = {{\n'
                element_str += \
                    self.__device_loc_to_c(
                        element.device_loc, indent='            ') + '\n'
                element_str += f'        }},\n'
                element_str += f'        .cert_loc = {{\n'
                element_str += self.__cert_loc_to_c(
                    element.cert_loc, indent='            ') + '\n'
                element_str += f'        }},\n'
                element_str += f'        .transforms = {{\n'
                element_str += ',\n'.join(
                    [f'            {cal.atcacert_transform_t(v).name}'
                        for v in element.transforms]) + '\n'
                element_str += f'        }}\n'
                element_str += f'    }}'
                element_strs.append(element_str)

            c_file += \
                f'const atcacert_cert_element_t {elements_var_name}[{self.cert_def.cert_elements_count}] = {{\n'
            c_file += ',\n'.join(element_strs) + '\n'
            c_file += '};\n'
            c_file += '\n'

        c_file += f'const atcacert_def_t {cert_def_var_name} = {{\n'
        c_file += f'    .type = {cal.atcacert_cert_type_t(self.cert_def.type).name},\n'
        c_file += f'    .template_id = {self.cert_def.template_id},\n'
        c_file += f'    .chain_id = {self.cert_def.chain_id},\n'
        c_file += f'    .private_key_slot = {self.cert_def.private_key_slot},\n'
        c_file += f'    .sn_source = {cal.atcacert_cert_sn_src_t(self.cert_def.sn_source).name},\n'
        c_file += f'    .cert_sn_dev_loc = {{\n'
        c_file += self.__device_loc_to_c(
            self.cert_def.cert_sn_dev_loc,
            indent='        ') + '\n'
        c_file += f'    }},\n'
        date_format = self.cert_def.issue_date_format
        c_file += f'    .issue_date_format = {cal.atcacert_date_format_t(date_format).name},\n'
        date_format = self.cert_def.expire_date_format
        c_file += f'    .expire_date_format = {cal.atcacert_date_format_t(date_format).name},\n'
        c_file += f'    .tbs_cert_loc = {{\n'
        c_file += self.__cert_loc_to_c(
            self.cert_def.tbs_cert_loc,
            indent='        ') + '\n'
        c_file += f'    }},\n'
        c_file += f'    .expire_years = {self.cert_def.expire_years},\n'
        c_file += f'    .public_key_dev_loc = {{\n'
        c_file += self.__device_loc_to_c(
            self.cert_def.public_key_dev_loc,
            indent='        ') + '\n'
        c_file += f'    }},\n'
        c_file += f'    .comp_cert_dev_loc = {{\n'
        c_file += self.__device_loc_to_c(
            self.cert_def.comp_cert_dev_loc,
            indent='        ') + '\n'
        c_file += f'    }},\n'
        std_element_names = [
            'STDCERT_PUBLIC_KEY',
            'STDCERT_SIGNATURE',
            'STDCERT_ISSUE_DATE',
            'STDCERT_EXPIRE_DATE',
            'STDCERT_SIGNER_ID',
            'STDCERT_CERT_SN',
            'STDCERT_AUTH_KEY_ID',
            'STDCERT_SUBJ_KEY_ID'
        ]
        c_file += f'    .std_cert_elements = {{\n'
        for i, name in enumerate(std_element_names):
            c_file += f'        {{ // {name}\n'
            c_file += self.__cert_loc_to_c(
                self.cert_def.std_cert_elements[i],
                indent='            ') + '\n'
            c_file += f'        }},\n'
        c_file += f'    }},\n'
        if self.cert_def.cert_elements:
            c_file += f'    .cert_elements = {elements_var_name},\n'
            c_file += f'    .cert_elements_count = sizeof({elements_var_name}) / sizeof({elements_var_name}[0]),\n'
        else:
            c_file += f'    .cert_elements = NULL,\n'
            c_file += f'    .cert_elements_count = 0,\n'
        c_file += f'    .cert_template = {template_var_name},\n'
        c_file += f'    .cert_template_size = sizeof({template_var_name}),\n'
        if self.ca_cert_def_var_name:
            c_file += f'    .ca_cert_def = &{self.ca_cert_def_var_name}\n'
        else:
            c_file += f'    .ca_cert_def = NULL\n'
        c_file += f'}};\n'

        h_file = ''
        h_file += f'#ifndef {self.filename_base.upper()}_H\n'
        h_file += f'#define {self.filename_base.upper()}_H\n'
        h_file += f'\n'
        h_file += f'#include "atcacert/atcacert_def.h"\n'
        h_file += f'\n'
        h_file += f'#ifdef __cplusplus\n'
        h_file += f'extern "C" {{\n'
        h_file += f'#endif\n'
        h_file += f'extern const atcacert_def_t {cert_def_var_name};\n'
        if self.chain_level == 1:
            h_file += f'extern const uint8_t {pk_var_name}[];\n'
        h_file += f'#ifdef __cplusplus\n'
        h_file += f'}}\n'
        h_file += f'#endif\n'
        h_file += '\n'
        h_file += '#endif\n'

        return {
            f'{self.filename_base}.c': c_file.encode('utf-8'),
            f'{self.filename_base}.h': h_file.encode('utf-8')
        }

    def get_cert_params(self):
        template_data = self.cert.public_bytes(
            encoding=serialization.Encoding.DER)
        asn1_cert = asn1crypto.x509.Certificate().load(
            template_data, strict=True)

        tbs_offset, tbs_count = tbs_location(asn1_cert)
        expire_years = self.cert.not_valid_after.year \
            - self.cert.not_valid_before.year
        if expire_years > 31:
            expire_years = 0  # Assume no expiration
        pk_offset, pk_count = public_key_location(asn1_cert)
        sig_offset, sig_count = signature_location(asn1_cert)
        nb_offset, nb_count = validity_location(asn1_cert, 'not_before')
        na_offset, na_count = validity_location(asn1_cert, 'not_after')
        sid_offset, sid_count = name_search_location_last(
            cert=asn1_cert,
            name='issuer' if self.chain_level == 0 else 'subject',
            search=self.signer_id
        )
        sn_offset, sn_count = sn_location(asn1_cert)
        akid_offset, akid_count = auth_key_id_location(asn1_cert)
        skid_offset, skid_count = subj_key_id_location(asn1_cert)
        if self.device_name == 'ECC204':
            public_key_dev_loc = {
                    'zone': cal.atcacert_device_zone_t.DEVZONE_DATA,
                    'slot': 0 if self.chain_level == 0 else 1,
                    'is_genkey': 1 if self.chain_level == 0 else 0,
                    'offset': 0 if self.chain_level == 0 else 128,
                    'count': 64}
            comp_cert_dev_loc = {
                    'zone': cal.atcacert_device_zone_t.DEVZONE_DATA,
                    'slot': 1,
                    'is_genkey': 0,
                    'offset': 0 if self.chain_level == 0 else 192,
                    'count': 72}
        else:
            public_key_dev_loc = {
                    'zone': cal.atcacert_device_zone_t.DEVZONE_DATA,
                    'slot': 0 if self.chain_level == 0 else 11,
                    'is_genkey': 1 if self.chain_level == 0 else 0,
                    'offset': 0,
                    'count': 64 if self.chain_level == 0 else 72}
            comp_cert_dev_loc = {
                    'zone': cal.atcacert_device_zone_t.DEVZONE_DATA,
                    'slot': 10 if self.chain_level == 0 else 12,
                    'is_genkey': 0,
                    'offset': 0,
                    'count': 72}

        params = {
            'type': cal.atcacert_cert_type_t.CERTTYPE_X509,
            'template_id': self.template_id,
            'chain_id': self.chain_id,
            'private_key_slot': 0,
            'sn_source': cal.atcacert_cert_sn_src_t.SNSRC_PUB_KEY_HASH,
            'cert_sn_dev_loc': {
                'zone': cal.atcacert_device_zone_t.DEVZONE_NONE,
                'slot': 0,
                'is_genkey': 0,
                'offset': 0,
                'count': 0,
            },
            'issue_date_format':
                cal.atcacert_date_format_t.DATEFMT_RFC5280_UTC,
            'expire_date_format':
                cal.atcacert_date_format_t.DATEFMT_RFC5280_GEN,
            'tbs_cert_loc': {
                'offset': tbs_offset,
                'count': tbs_count
            },
            'expire_years': expire_years,
            'public_key_dev_loc': public_key_dev_loc,
            'comp_cert_dev_loc': comp_cert_dev_loc,
            'std_cert_elements': [
                # STDCERT_PUBLIC_KEY
                {'offset': pk_offset, 'count': pk_count},
                # STDCERT_SIGNATURE
                {'offset': sig_offset, 'count': sig_count},
                # STDCERT_ISSUE_DATE
                {'offset': nb_offset, 'count': nb_count},
                # STDCERT_EXPIRE_DATE
                {'offset': na_offset, 'count': na_count},
                # STDCERT_SIGNER_ID
                {'offset': sid_offset, 'count': sid_count},
                # STDCERT_CERT_SN
                {'offset': sn_offset, 'count': sn_count},
                # STDCERT_AUTH_KEY_ID
                {'offset': akid_offset, 'count': akid_count},
                # STDCERT_SUBJ_KEY_ID
                {'offset': skid_offset, 'count': skid_count}
            ],
            'ca_cert_def':
                pointer(self.ca_cert_def) if self.ca_cert_def else None
        }
        return params

    def get_cert_elements(self):
        template_data = \
            self.cert.public_bytes(encoding=serialization.Encoding.DER)
        asn1_cert = \
            asn1crypto.x509.Certificate().load(template_data, strict=True)

        elements = []
        if self.serial_num is not None:
            if self.device_name == 'ECC204':
                sn_offset, sn_count = name_search_location(
                    asn1_cert, 'subject', self.serial_num[0:18])
                elements.append(
                    {
                        'id': 'SN08',
                        'device_loc': {
                            'zone': cal.atcacert_device_zone_t.DEVZONE_CONFIG,
                            'slot': 0,
                            'is_genkey': 0,
                            'offset': 0,
                            'count': 9
                        },
                        'cert_loc': {
                            'offset': sn_offset,
                            'count': sn_count
                        },
                        'transforms': [
                            cal.atcacert_transform_t.TF_BIN2HEX_UC,
                            cal.atcacert_transform_t.TF_NONE
                        ]
                    }
                )
            else:
                sn03_offset, sn03_count = name_search_location(
                    asn1_cert, 'subject', self.serial_num[0:8])
                elements.append(
                    {
                        'id': 'SN03',
                        'device_loc': {
                            'zone': cal.atcacert_device_zone_t.DEVZONE_CONFIG,
                            'slot': 0,
                            'is_genkey': 0,
                            'offset': 0,
                            'count': 4
                        },
                        'cert_loc': {
                            'offset': sn03_offset,
                            'count': sn03_count
                        },
                        'transforms': [
                            cal.atcacert_transform_t.TF_BIN2HEX_UC,
                            cal.atcacert_transform_t.TF_NONE
                        ]
                    }
                )
                sn48_offset, sn48_count = name_search_location(
                    asn1_cert, 'subject', self.serial_num[8:18])
                elements.append(
                    {
                        'id': 'SN48',
                        'device_loc': {
                            'zone': cal.atcacert_device_zone_t.DEVZONE_CONFIG,
                            'slot': 0,
                            'is_genkey': 0,
                            'offset': 8,
                            'count': 5
                        },
                        'cert_loc': {
                            'offset': sn48_offset,
                            'count': sn48_count
                        },
                        'transforms': [
                            cal.atcacert_transform_t.TF_BIN2HEX_UC,
                            cal.atcacert_transform_t.TF_NONE
                        ]
                    }
                )
        return elements

    def __get_signer_template(self, cert):
        signer = CertDef(self.device_name)
        signer.set_certificate(cert, None)
        return signer.__build_py_definition()

    @staticmethod
    def __params_atcacert_definitions(template_data, params, elements):
        cert_def = cal.atcacert_def_t(**params)
        cert_def.cert_template_size = len(template_data)
        cert_def.cert_template = cast(create_string_buffer(
            template_data, cert_def.cert_template_size), POINTER(c_uint8))

        if elements:
            cert_def.cert_elements_count = len(elements)
            elems = [cal.atcacert_cert_element_t(**x) for x in elements]
            elems_array = \
                (cal.atcacert_cert_element_t * cert_def.cert_elements_count)(
                    *elems)
            cert_def.cert_elements = cast(elems_array, POINTER(
                cal.atcacert_cert_element_t))
        return cert_def

    @staticmethod
    def __device_loc_to_c(device_loc, indent=''):
        lines = [
            f'.zone = {cal.atcacert_device_zone_t(device_loc.zone).name}',
            f'.slot = {device_loc.slot}',
            f'.is_genkey = {device_loc.is_genkey}',
            f'.offset = {device_loc.offset}',
            f'.count = {device_loc.count}',
        ]

        return ',\n'.join([f'{indent}{line}' for line in lines])

    @staticmethod
    def __cert_loc_to_c(cert_loc, indent=''):
        lines = [
            f'.offset = {cert_loc.offset}',
            f'.count = {cert_loc.count}',
        ]

        return ',\n'.join([f'{indent}{line}' for line in lines])

    @staticmethod
    def __c_hex_array(data, indent='    ', bytes_per_line=16):
        lines = []
        for i in range(0, len(data), bytes_per_line):
            lines.append(indent + ', '.join([
                f'0x{v:02x}' for v in data[i:i+bytes_per_line]]) + ',')
        return '{\n' + '\n'.join(lines) + '\n}'

    @staticmethod
    def __get_signer_id(cert):
        """
        Get the signer id from the certificate.
        """
        for attr in cert.subject:
            if attr.oid == x509.oid.NameOID.COMMON_NAME:
                signer_id = attr.value[-4:]
                if re.search('^[0-9A-F]{4}$', signer_id) is None:
                    raise ValueError(
                            'signer_id={} must be 4 uppercase hex digits'
                            .format(signer_id))
                return signer_id
