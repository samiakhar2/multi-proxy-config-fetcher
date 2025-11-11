import json
import base64
import sys
import os
from typing import Dict, Optional, List
from urllib.parse import urlparse, parse_qs, unquote
import logging
import re
import binascii
import config_parser as parser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COUNTRY_CODES = {
    'United States': 'US', 'United Kingdom': 'GB', 'Germany': 'DE', 'France': 'FR',
    'Canada': 'CA', 'Australia': 'AU', 'Netherlands': 'NL', 'Sweden': 'SE',
    'Switzerland': 'CH', 'Singapore': 'SG', 'Japan': 'JP', 'South Korea': 'KR',
    'Hong Kong': 'HK', 'Taiwan': 'TW', 'India': 'IN', 'Russia': 'RU',
    'Brazil': 'BR', 'Mexico': 'MX', 'Argentina': 'AR', 'Spain': 'ES',
    'Italy': 'IT', 'Poland': 'PL', 'Turkey': 'TR', 'Ukraine': 'UA',
    'Finland': 'FI', 'Norway': 'NO', 'Denmark': 'DK', 'Belgium': 'BE',
    'Austria': 'AT', 'Czech Republic': 'CZ', 'Ireland': 'IE', 'Portugal': 'PT',
    'Greece': 'GR', 'Romania': 'RO', 'Bulgaria': 'BG', 'Hungary': 'HU',
    'Israel': 'IL', 'United Arab Emirates': 'AE', 'Saudi Arabia': 'SA',
    'South Africa': 'ZA', 'Egypt': 'EG', 'Nigeria': 'NG', 'Kenya': 'KE',
    'China': 'CN', 'Thailand': 'TH', 'Vietnam': 'VN', 'Philippines': 'PH',
    'Indonesia': 'ID', 'Malaysia': 'MY', 'New Zealand': 'NZ',
    'Chile': 'CL', 'Colombia': 'CO', 'Peru': 'PE', 'Venezuela': 'VE',
    'Iran': 'IR', 'Iraq': 'IQ', 'Pakistan': 'PK', 'Bangladesh': 'BD',
    'Kazakhstan': 'KZ', 'Uzbekistan': 'UZ', 'Azerbaijan': 'AZ',
    'Latvia': 'LV', 'Lithuania': 'LT', 'Estonia': 'EE', 'Iceland': 'IS',
    'Luxembourg': 'LU', 'Malta': 'MT', 'Cyprus': 'CY', 'Croatia': 'HR',
    'Serbia': 'RS', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Moldova': 'MD',
    'United States of America': 'US', 'Kingdom of the Netherlands': 'NL',
    'Turkiye': 'TR', 'Czechia': 'CZ', 'Viet Nam': 'VN', 'Panama': 'PA',
    'United Kingdom of Great Britain and Northern Ireland': 'GB',
    'Taiwan (Province of China)': 'TW',
    'Unknown': 'XX'
}

class ConfigRenamer:
    def __init__(self, location_file: str):
        self.location_cache: Dict[str, tuple] = {}
        self.load_location_cache(location_file)

    def load_location_cache(self, location_file: str):
        try:
            with open(location_file, 'r', encoding='utf-8') as f:
                self.location_cache = json.load(f)
            logger.info(f"Loaded {len(self.location_cache)} location entries from cache")
        except FileNotFoundError:
            logger.error(f"{location_file} not found!")
        except Exception as e:
            logger.error(f"Error loading location cache: {e}")

    def get_location(self, address: str) -> tuple:
        if address in self.location_cache:
            flag, country = tuple(self.location_cache[address])
            country_code = COUNTRY_CODES.get(country, 'XX')
            return flag, country_code
        return "🏳️", "XX"

    def build_protocol_info(self, protocol_type: str, data: Dict) -> List[str]:
        info_parts = [protocol_type]
        
        if protocol_type == "VMess":
            net_type = data.get('net', 'tcp').lower()
            tls = data.get('tls', 'none').lower()
            
            if net_type == 'ws':
                info_parts.append('WS')
            elif net_type == 'grpc':
                info_parts.append('GRPC')
            elif net_type == 'http' or net_type == 'h2':
                info_parts.append('HTTP2')
            elif net_type == 'quic':
                info_parts.append('QUIC')
            elif net_type == 'kcp':
                info_parts.append('KCP')
            elif net_type == 'splithttp':
                info_parts.append('SPLITHTTP')
            elif net_type == 'xhttp':
                info_parts.append('XHTTP')
            elif net_type == 'httpupgrade':
                info_parts.append('HTTPUPGRADE')
            
            if tls == 'tls':
                info_parts.append('TLS')
            
            if data.get('fp'):
                info_parts.append('UTLS')
        
        elif protocol_type == "VLESS":
            transport_type = data.get('type', 'tcp').lower()
            security = data.get('security', 'none').lower()
            flow = data.get('flow', '').lower()
            
            if transport_type == 'ws':
                info_parts.append('WS')
            elif transport_type == 'grpc':
                info_parts.append('GRPC')
            elif transport_type == 'http' or transport_type == 'h2':
                info_parts.append('HTTP2')
            elif transport_type == 'quic':
                info_parts.append('QUIC')
            elif transport_type == 'kcp':
                info_parts.append('KCP')
            elif transport_type == 'splithttp':
                info_parts.append('SPLITHTTP')
            elif transport_type == 'xhttp':
                info_parts.append('XHTTP')
            elif transport_type == 'httpupgrade':
                info_parts.append('HTTPUPGRADE')
            elif transport_type == 'raw':
                info_parts.append('RAW')

            if security == 'reality':
                info_parts.append('REALITY')
                if data.get('pbk'):
                    info_parts.append('PQ')
            elif security == 'tls':
                info_parts.append('TLS')
            elif security == 'xtls':
                info_parts.append('XTLS')
            
            if 'vision' in flow:
                info_parts.append('VISION')
            elif 'xtls-rprx-direct' in flow:
                info_parts.append('DIRECT')
            elif 'xtls' in flow:
                info_parts.append('XTLS-FLOW')
            
            if data.get('fp'):
                info_parts.append('UTLS')
        
        elif protocol_type == "Trojan":
            transport_type = data.get('type', 'tcp').lower()
            flow = data.get('flow', '').lower()
            
            if transport_type == 'ws':
                info_parts.append('WS')
            elif transport_type == 'grpc':
                info_parts.append('GRPC')
            elif transport_type == 'quic':
                info_parts.append('QUIC')
            elif transport_type == 'kcp':
                info_parts.append('KCP')
            elif transport_type == 'splithttp':
                info_parts.append('SPLITHTTP')
            elif transport_type == 'xhttp':
                info_parts.append('XHTTP')
            elif transport_type == 'httpupgrade':
                info_parts.append('HTTPUPGRADE')
            elif transport_type == 'http' or transport_type == 'h2':
                info_parts.append('HTTP2')
                
            info_parts.append('TLS')
            
            if 'vision' in flow:
                info_parts.append('VISION')
            elif 'xtls' in flow:
                info_parts.append('XTLS')
            
            if data.get('fp'):
                info_parts.append('UTLS')
        
        elif protocol_type == "Hysteria2":
            info_parts.append('QUIC')
            obfs = data.get('obfs', '')
            if obfs:
                info_parts.append('OBFS')
        
        elif protocol_type == "SS":
            method = data.get('method', '').lower()
            if '2022' in method:
                info_parts.append('2022')
                if 'blake3' in method:
                    info_parts.append('BLAKE3')
            elif 'gcm' in method or 'poly1305' in method:
                info_parts.append('AEAD')
            else:
                info_parts.append('STREAM')
        
        return info_parts

    def rename_config(self, config: str, index: int, protocol_type: str) -> Optional[str]:
        try:
            config_lower = config.lower()
            
            if config_lower.startswith('vmess://'):
                data = parser.decode_vmess(config)
                if not data or not all(k in data for k in ['add', 'port', 'id']):
                    return None
                flag, country_code = self.get_location(data['add'])
                protocol_info = self.build_protocol_info(protocol_type, data)
                protocol_str = '/'.join(protocol_info)
                new_name = f"{flag} {index} - {country_code} - {protocol_str} - {data['port']}"
                data['ps'] = new_name
                encoded = base64.b64encode(json.dumps(data, ensure_ascii=False).encode('utf-8')).decode('utf-8')
                return f"vmess://{encoded}"
            
            elif config_lower.startswith('vless://'):
                data = parser.parse_vless(config)
                if not data:
                    return None
                flag, country_code = self.get_location(data['address'])
                protocol_info = self.build_protocol_info(protocol_type, data)
                protocol_str = '/'.join(protocol_info)
                new_name = f"{flag} {index} - {country_code} - {protocol_str} - {data['port']}"
                url = urlparse(config)
                params = parse_qs(url.query)
                query_string = '&'.join([f"{k}={v[0]}" for k, v in params.items()])
                new_config = f"vless://{data['uuid']}@{data['address']}:{data['port']}?{query_string}#{new_name}"
                return new_config
            
            elif config_lower.startswith('trojan://'):
                data = parser.parse_trojan(config)
                if not data:
                    return None
                flag, country_code = self.get_location(data['address'])
                protocol_info = self.build_protocol_info(protocol_type, data)
                protocol_str = '/'.join(protocol_info)
                new_name = f"{flag} {index} - {country_code} - {protocol_str} - {data['port']}"
                url = urlparse(config)
                params = parse_qs(url.query)
                query_string = '&'.join([f"{k}={v[0]}" for k, v in params.items()])
                new_config = f"trojan://{data['password']}@{data['address']}:{data['port']}?{query_string}#{new_name}"
                return new_config
            
            elif config_lower.startswith(('hysteria2://', 'hy2://')):
                data = parser.parse_hysteria2(config)
                if not data:
                    return None
                flag, country_code = self.get_location(data['address'])
                protocol_info = self.build_protocol_info(protocol_type, data)
                protocol_str = '/'.join(protocol_info)
                new_name = f"{flag} {index} - {country_code} - {protocol_str} - {data['port']}"
                url = urlparse(config)
                query_string = url.query
                protocol = 'hysteria2' if config_lower.startswith('hysteria2://') else 'hy2'
                new_config = f"{protocol}://{data['password']}@{data['address']}:{data['port']}?{query_string}#{new_name}"
                return new_config
            
            elif config_lower.startswith('ss://'):
                data = parser.parse_shadowsocks(config)
                if not data:
                    return None
                flag, country_code = self.get_location(data['address'])
                protocol_info = self.build_protocol_info(protocol_type, data)
                protocol_str = '/'.join(protocol_info)
                new_name = f"{flag} {index} - {country_code} - {protocol_str} - {data['port']}"
                method_pass = f"{data['method']}:{data['password']}"
                encoded = base64.b64encode(method_pass.encode('utf-8')).decode('utf-8').replace('+', '-').replace('/', '_').rstrip('=')
                new_config = f"ss://{encoded}@{data['address']}:{data['port']}#{new_name}"
                return new_config
            
            return None
        except Exception as e:
            logger.error(f"Failed to rename config: {e}")
            return None

    def process_configs(self, input_file: str, output_file: str):
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            logger.error(f"{input_file} not found!")
            return
        except Exception as e:
            logger.error(f"Error reading {input_file}: {e}")
            return

        renamed_configs = []
        header_lines = []
        configs = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('//') or not line:
                if not configs:
                    header_lines.append(line)
            else:
                configs.append(line)

        counters = {"VLESS": 1, "Trojan": 1, "VMess": 1, "SS": 1, "Hysteria2": 1}
        protocol_map = {'vless': 'VLESS', 'trojan': 'Trojan', 'vmess': 'VMess', 'ss': 'SS', 'hysteria2': 'Hysteria2', 'hy2': 'Hysteria2'}

        for config in configs:
            protocol_key = config.split('://')[0].lower()
            protocol_name = protocol_map.get(protocol_key)
            
            if protocol_name:
                renamed = self.rename_config(config, counters[protocol_name], protocol_name)
                if renamed:
                    renamed_configs.append(renamed)
                    counters[protocol_name] += 1
                else:
                    logger.warning(f"Could not parse or rename config, appending as-is: {config[:40]}...")
                    renamed_configs.append(config)
            else:
                renamed_configs.append(config)

        try:
            os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                for header in header_lines:
                    f.write(header + '\n')
                if header_lines and renamed_configs:
                    f.write('\n')
                for config in renamed_configs:
                    f.write(config + '\n\n')
            logger.info(f"Successfully renamed {len(renamed_configs)} configs and saved to {output_file}")
        except IOError as e:
            logger.error(f"Failed to write output file: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")


def main():
    if len(sys.argv) < 4:
        print("Usage: python rename_configs.py <location.json> <input.txt> <output.txt>")
        sys.exit(1)
    
    location_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    renamer = ConfigRenamer(location_file)
    renamer.process_configs(input_file, output_file)

if __name__ == '__main__':
    main()