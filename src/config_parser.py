import json
import base64
import re
from typing import Dict, Optional
from urllib.parse import urlparse, parse_qs, unquote
import binascii

def is_base64(s: str) -> bool:
    try:
        s = s.rstrip('=')
        return bool(re.match(r'^[A-Za-z0-9+/\-_]*$', s))
    except:
        return False

def decode_vmess(config: str) -> Optional[Dict]:
    try:
        encoded = config.replace('vmess://', '')
        padding = '=' * (-len(encoded) % 4)
        decoded = base64.b64decode(encoded + padding).decode('utf-8')
        data = json.loads(decoded)
        data['name'] = data.get('ps')
        return data
    except (json.JSONDecodeError, binascii.Error, UnicodeDecodeError):
        return None

def parse_vless(config: str) -> Optional[Dict]:
    try:
        url = urlparse(config)
        if url.scheme.lower() != 'vless' or not url.hostname:
            return None
        netloc = url.netloc.split('@')[-1]
        address, port = netloc.split(':') if ':' in netloc else (netloc, '443')
        params = parse_qs(url.query)
        return {
            'uuid': url.username,
            'address': address,
            'port': int(port),
            'flow': params.get('flow', [''])[0],
            'sni': params.get('sni', [address])[0],
            'type': params.get('type', ['tcp'])[0],
            'path': params.get('path', [''])[0],
            'host': params.get('host', [address])[0],
            'security': params.get('security', ['none'])[0],
            'alpn': params.get('alpn', [''])[0],
            'fp': params.get('fp', [''])[0],
            'pbk': params.get('pbk', [''])[0],
            'sid': params.get('sid', [''])[0],
            'spx': params.get('spx', [''])[0],
            'name': unquote(url.fragment) if url.fragment else None
        }
    except (ValueError, TypeError, AttributeError):
        return None

def parse_trojan(config: str) -> Optional[Dict]:
    try:
        url = urlparse(config)
        if url.scheme.lower() != 'trojan' or not url.hostname:
            return None
        port = url.port or 443
        params = parse_qs(url.query)
        return {
            'password': url.username,
            'address': url.hostname,
            'port': port,
            'sni': params.get('sni', [url.hostname])[0],
            'alpn': params.get('alpn', [''])[0],
            'type': params.get('type', ['tcp'])[0],
            'path': params.get('path', [''])[0],
            'host': params.get('host', [url.hostname])[0],
            'security': params.get('security', ['tls'])[0],
            'fp': params.get('fp', [''])[0],
            'flow': params.get('flow', [''])[0],
            'name': unquote(url.fragment) if url.fragment else None
        }
    except (ValueError, TypeError, AttributeError):
        return None

def parse_hysteria2(config: str) -> Optional[Dict]:
    try:
        url = urlparse(config)
        if url.scheme.lower() not in ['hysteria2', 'hy2'] or not url.hostname or not url.port:
            return None
        params = parse_qs(url.query)
        return {
            'address': url.hostname,
            'port': url.port,
            'password': url.username or params.get('password', [''])[0],
            'sni': params.get('sni', [url.hostname])[0],
            'obfs': params.get('obfs', [''])[0],
            'insecure': params.get('insecure', ['0'])[0],
            'name': unquote(url.fragment) if url.fragment else None
        }
    except (ValueError, TypeError, AttributeError):
        return None

def parse_shadowsocks(config: str) -> Optional[Dict]:
    try:
        url = urlparse(config)
        if url.scheme.lower() != 'ss':
            return None
        
        if '@' not in url.netloc:
            return None
        
        credential_part, server_part = url.netloc.split('@', 1)
        host, port_str = server_part.rsplit(':', 1)
        port = int(port_str)

        credential_part_unquoted = unquote(credential_part)
        if is_base64(credential_part_unquoted):
            method_pass_b64 = credential_part_unquoted.replace('-', '+').replace('_', '/')
            padding = '=' * (-len(method_pass_b64) % 4)
            method_pass = base64.b64decode(method_pass_b64 + padding).decode('utf-8')
            method, password = method_pass.split(':', 1)
        else:
            method, password = credential_part_unquoted.split(':', 1)
        
        return {
            'method': method,
            'password': password,
            'address': host,
            'port': int(port),
            'name': unquote(url.fragment) if url.fragment else None
        }
    except (ValueError, TypeError, AttributeError, binascii.Error, UnicodeDecodeError):
        return None
