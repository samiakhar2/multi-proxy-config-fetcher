import json
import base64
import re
from typing import Dict, Optional
from urllib.parse import urlparse, parse_qs, unquote
import binascii
from functools import lru_cache

VALID_UUID_PATTERN = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
VALID_IPV4_PATTERN = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
VALID_IPV6_PATTERN = re.compile(r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}$|^[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}$')
VALID_DOMAIN_PATTERN = re.compile(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$')

VALID_SS_METHODS = {
    'aes-128-gcm', 'aes-192-gcm', 'aes-256-gcm',
    'chacha20-ietf-poly1305', 'xchacha20-ietf-poly1305',
    '2022-blake3-aes-128-gcm', '2022-blake3-aes-256-gcm',
    'aes-128-cfb', 'aes-192-cfb', 'aes-256-cfb',
    'aes-128-ctr', 'aes-192-ctr', 'aes-256-ctr',
    'chacha20', 'chacha20-ietf', 'rc4-md5'
}

VALID_VLESS_FLOWS = {'', 'xtls-rprx-origin', 'xtls-rprx-direct', 'xtls-rprx-vision'}
VALID_VLESS_SECURITY = {'none', 'tls', 'reality', 'xtls'}
VALID_TRANSPORT_TYPES = {'tcp', 'kcp', 'ws', 'http', 'h2', 'quic', 'grpc', 'httpupgrade', 'splithttp', 'xhttp', 'raw'}

def is_base64(s: str) -> bool:
    try:
        if not s or len(s) < 4:
            return False
        s = s.rstrip('=')
        return bool(re.match(r'^[A-Za-z0-9+/\-_]+$', s)) and len(s) % 4 in (0, 2, 3)
    except Exception:
        return False

@lru_cache(maxsize=1024)
def safe_b64decode(s: str) -> Optional[str]:
    try:
        if not s:
            return None
        s = s.replace('-', '+').replace('_', '/')
        padding = '=' * (-len(s) % 4)
        decoded = base64.b64decode(s + padding)
        return decoded.decode('utf-8')
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return None

def validate_uuid(uuid: str) -> bool:
    return bool(VALID_UUID_PATTERN.match(uuid))

def validate_host(host: str) -> bool:
    if not host:
        return False
    if VALID_IPV4_PATTERN.match(host):
        return True
    if VALID_IPV6_PATTERN.match(host):
        return True
    if VALID_DOMAIN_PATTERN.match(host):
        return True
    return False

def validate_port(port: int) -> bool:
    return isinstance(port, int) and 1 <= port <= 65535

def decode_vmess(config: str) -> Optional[Dict]:
    try:
        if not config or not config.startswith('vmess://'):
            return None
        encoded = config[8:].strip()
        if not encoded:
            return None
        decoded = safe_b64decode(encoded)
        if not decoded:
            return None
        data = json.loads(decoded)
        if not isinstance(data, dict):
            return None
        required_fields = ['add', 'port', 'id']
        if not all(field in data and data[field] for field in required_fields):
            return None
        if not validate_host(data['add']):
            return None
        try:
            port = int(data['port'])
            if not validate_port(port):
                return None
            data['port'] = port
        except (ValueError, TypeError):
            return None
        if not validate_uuid(data['id']):
            return None
        data['name'] = data.get('ps', data.get('name', ''))
        data['net'] = data.get('net', 'tcp').lower()
        data['tls'] = data.get('tls', 'none').lower()
        if data['net'] not in VALID_TRANSPORT_TYPES:
            data['net'] = 'tcp'
        return data
    except (json.JSONDecodeError, TypeError, KeyError, AttributeError):
        return None

def parse_vless(config: str) -> Optional[Dict]:
    try:
        if not config or not config.startswith('vless://'):
            return None
        url = urlparse(config)
        if not url.hostname or not url.username:
            return None
        if not validate_uuid(url.username):
            return None
        if not validate_host(url.hostname):
            return None
        port = url.port or 443
        if not validate_port(port):
            return None
        params = parse_qs(url.query)
        security = params.get('security', ['none'])[0].lower()
        if security not in VALID_VLESS_SECURITY:
            security = 'none'
        flow = params.get('flow', [''])[0].lower()
        if flow and flow not in VALID_VLESS_FLOWS:
            flow = ''
        transport_type = params.get('type', ['tcp'])[0].lower()
        if transport_type not in VALID_TRANSPORT_TYPES:
            transport_type = 'tcp'
        return {
            'uuid': url.username,
            'address': url.hostname,
            'port': port,
            'flow': flow,
            'sni': params.get('sni', [url.hostname])[0],
            'type': transport_type,
            'path': params.get('path', [''])[0],
            'host': params.get('host', [url.hostname])[0],
            'security': security,
            'alpn': params.get('alpn', [''])[0],
            'fp': params.get('fp', [''])[0],
            'pbk': params.get('pbk', [''])[0],
            'sid': params.get('sid', [''])[0],
            'spx': params.get('spx', [''])[0],
            'name': unquote(url.fragment) if url.fragment else ''
        }
    except (ValueError, TypeError, AttributeError):
        return None

def parse_trojan(config: str) -> Optional[Dict]:
    try:
        if not config or not config.startswith('trojan://'):
            return None
        url = urlparse(config)
        if not url.hostname or not url.username:
            return None
        if not validate_host(url.hostname):
            return None
        port = url.port or 443
        if not validate_port(port):
            return None
        params = parse_qs(url.query)
        transport_type = params.get('type', ['tcp'])[0].lower()
        if transport_type not in VALID_TRANSPORT_TYPES:
            transport_type = 'tcp'
        return {
            'password': url.username,
            'address': url.hostname,
            'port': port,
            'sni': params.get('sni', [url.hostname])[0],
            'alpn': params.get('alpn', [''])[0],
            'type': transport_type,
            'path': params.get('path', [''])[0],
            'host': params.get('host', [url.hostname])[0],
            'security': params.get('security', ['tls'])[0],
            'fp': params.get('fp', [''])[0],
            'flow': params.get('flow', [''])[0],
            'name': unquote(url.fragment) if url.fragment else ''
        }
    except (ValueError, TypeError, AttributeError):
        return None

def parse_hysteria2(config: str) -> Optional[Dict]:
    try:
        if not config or not config.startswith(('hysteria2://', 'hy2://')):
            return None
        url = urlparse(config)
        if not url.hostname:
            return None
        if not validate_host(url.hostname):
            return None
        port = url.port or 443
        if not validate_port(port):
            return None
        params = parse_qs(url.query)
        password = url.username or params.get('password', [''])[0]
        if not password:
            return None
        return {
            'address': url.hostname,
            'port': port,
            'password': password,
            'sni': params.get('sni', [url.hostname])[0],
            'obfs': params.get('obfs', [''])[0],
            'obfs-password': params.get('obfs-password', [''])[0],
            'insecure': params.get('insecure', ['0'])[0],
            'pinSHA256': params.get('pinSHA256', [''])[0],
            'name': unquote(url.fragment) if url.fragment else ''
        }
    except (ValueError, TypeError, AttributeError):
        return None

def parse_shadowsocks(config: str) -> Optional[Dict]:
    try:
        if not config or not config.startswith('ss://'):
            return None
        url = urlparse(config)
        if '@' not in url.netloc:
            return None
        credential_part, server_part = url.netloc.split('@', 1)
        if ':' not in server_part:
            return None
        host, port_str = server_part.rsplit(':', 1)
        if not validate_host(host):
            return None
        try:
            port = int(port_str)
            if not validate_port(port):
                return None
        except ValueError:
            return None
        credential_part_unquoted = unquote(credential_part)
        if is_base64(credential_part_unquoted):
            method_pass = safe_b64decode(credential_part_unquoted)
            if not method_pass or ':' not in method_pass:
                return None
            method, password = method_pass.split(':', 1)
        else:
            if ':' not in credential_part_unquoted:
                return None
            method, password = credential_part_unquoted.split(':', 1)
        if not method or not password:
            return None
        method = method.lower().strip()
        if method not in VALID_SS_METHODS:
            return None
        params = parse_qs(url.query)
        plugin = params.get('plugin', [''])[0]
        return {
            'method': method,
            'password': password,
            'address': host,
            'port': port,
            'plugin': plugin,
            'name': unquote(url.fragment) if url.fragment else ''
        }
    except (ValueError, TypeError, AttributeError, IndexError):
        return None

def parse_wireguard(config: str) -> Optional[Dict]:
    try:
        if not config or not config.startswith('wireguard://'):
            return None
        url = urlparse(config)
        if not url.hostname:
            return None
        if not validate_host(url.hostname):
            return None
        port = url.port or 51820
        if not validate_port(port):
            return None
        params = parse_qs(url.query)
        private_key = url.username or params.get('privatekey', [''])[0]
        if not private_key:
            return None
        return {
            'address': url.hostname,
            'port': port,
            'private_key': private_key,
            'public_key': params.get('publickey', [''])[0],
            'preshared_key': params.get('presharedkey', [''])[0],
            'reserved': params.get('reserved', [''])[0],
            'mtu': params.get('mtu', ['1420'])[0],
            'local_address': params.get('address', [''])[0],
            'peers': params.get('peer', []),
            'name': unquote(url.fragment) if url.fragment else ''
        }
    except (ValueError, TypeError, AttributeError):
        return None

def parse_tuic(config: str) -> Optional[Dict]:
    try:
        if not config or not config.startswith('tuic://'):
            return None
        url = urlparse(config)
        if not url.hostname:
            return None
        if not validate_host(url.hostname):
            return None
        port = url.port or 443
        if not validate_port(port):
            return None
        if not url.username or ':' not in url.username:
            return None
        uuid, password = url.username.split(':', 1)
        if not validate_uuid(uuid):
            return None
        params = parse_qs(url.query)
        return {
            'address': url.hostname,
            'port': port,
            'uuid': uuid,
            'password': password,
            'congestion_control': params.get('congestion_control', ['bbr'])[0],
            'udp_relay_mode': params.get('udp_relay_mode', ['native'])[0],
            'alpn': params.get('alpn', ['h3'])[0],
            'sni': params.get('sni', [url.hostname])[0],
            'allow_insecure': params.get('allow_insecure', ['0'])[0],
            'disable_sni': params.get('disable_sni', ['0'])[0],
            'name': unquote(url.fragment) if url.fragment else ''
        }
    except (ValueError, TypeError, AttributeError):
        return None