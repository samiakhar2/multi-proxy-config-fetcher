import os
import json
import subprocess
import tempfile
import logging
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests
import signal
import socket
import sys
import base64
from urllib.parse import urlparse, parse_qs
from contextlib import closing
from config import ProxyConfig
import config_parser as parser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class XrayTester:
    def __init__(self, xray_path: str = 'xray', timeout: int = 10, test_urls: List[str] = None):
        self.xray_path = xray_path
        self.timeout = timeout
        self.test_urls = test_urls if test_urls else ['https://www.youtube.com/generate_204']
        self.unsupported_protocols = ['tuic://', 'wireguard://']
        
    def is_supported_protocol(self, config_str: str) -> bool:
        config_lower = config_str.lower()
        for protocol in self.unsupported_protocols:
            if config_lower.startswith(protocol):
                return False
        return True
        
    def parse_config_string(self, config_str: str) -> Optional[Dict]:
        try:
            config_lower = config_str.lower()
            
            if config_lower.startswith('vmess://'):
                data = parser.decode_vmess(config_str)
                if not data: return None
                
                outbound = {
                    "protocol": "vmess",
                    "settings": {
                        "vnext": [{
                            "address": data.get('add'),
                            "port": int(data.get('port')),
                            "users": [{
                                "id": data.get('id'),
                                "alterId": int(data.get('aid', 0)),
                                "security": data.get('scy', 'auto')
                            }]
                        }]
                    }
                }
                
                if data.get('net') == 'ws':
                    outbound["streamSettings"] = {
                        "network": "ws",
                        "wsSettings": {
                            "path": data.get('path', '/'),
                            "headers": {"Host": data.get('host', data['add'])}
                        }
                    }
                    
                if data.get('tls') == 'tls':
                    if "streamSettings" not in outbound:
                        outbound["streamSettings"] = {}
                    outbound["streamSettings"]["security"] = "tls"
                    outbound["streamSettings"]["tlsSettings"] = {
                        "serverName": data.get('sni', data['add']),
                        "allowInsecure": False
                    }
                    
                return outbound
            
            elif config_lower.startswith('vless://'):
                data = parser.parse_vless(config_str)
                if not data: return None
                
                outbound = {
                    "protocol": "vless",
                    "settings": {
                        "vnext": [{
                            "address": data['address'],
                            "port": data['port'],
                            "users": [{
                                "id": data['uuid'],
                                "encryption": "none",
                                "flow": data.get('flow', '')
                            }]
                        }]
                    }
                }
                
                net_type = data.get('type', 'tcp')
                if net_type == 'ws':
                    outbound["streamSettings"] = {
                        "network": "ws",
                        "wsSettings": {
                            "path": data.get('path', '/'),
                            "headers": {"Host": data.get('host', data['address'])}
                        }
                    }
                    
                security = data.get('security', 'none')
                if security == 'tls':
                    if "streamSettings" not in outbound:
                        outbound["streamSettings"] = {"network": "tcp"}
                    outbound["streamSettings"]["security"] = "tls"
                    outbound["streamSettings"]["tlsSettings"] = {
                        "serverName": data.get('sni', data['address']),
                        "allowInsecure": False
                    }
                    
                return outbound
                
            elif config_lower.startswith('trojan://'):
                data = parser.parse_trojan(config_str)
                if not data: return None
                
                outbound = {
                    "protocol": "trojan",
                    "settings": {
                        "servers": [{
                            "address": data['address'],
                            "port": data['port'],
                            "password": data['password']
                        }]
                    },
                    "streamSettings": {
                        "network": data.get('type', 'tcp'),
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": data.get('sni', data['address']),
                            "allowInsecure": False
                        }
                    }
                }
                
                if data.get('type', 'tcp') == 'ws':
                    outbound["streamSettings"]["wsSettings"] = {
                        "path": data.get('path', '/'),
                        "headers": {"Host": data.get('host', data['address'])}
                    }
                    
                return outbound
                
            elif config_lower.startswith('ss://'):
                data = parser.parse_shadowsocks(config_str)
                if not data: return None
                
                outbound = {
                    "protocol": "shadowsocks",
                    "settings": {
                        "servers": [{
                            "address": data['address'],
                            "port": data['port'],
                            "method": data['method'],
                            "password": data['password']
                        }]
                    }
                }
                
                return outbound
            
            return None
            
        except Exception as e:
            logger.warning(f"Failed to parse config: {str(e)}")
            return None
    
    def create_xray_config(self, outbound: Dict, socks_port: int, http_port: int) -> Dict:
        return {
            "log": {
                "loglevel": "error"
            },
            "inbounds": [
                {
                    "port": socks_port,
                    "protocol": "socks",
                    "settings": {
                        "auth": "noauth",
                        "udp": False
                    }
                },
                {
                    "port": http_port,
                    "protocol": "http"
                }
            ],
            "outbounds": [outbound]
        }
    
    def test_config(self, config_str: str) -> Tuple[bool, Optional[int], str]:
        if not self.is_supported_protocol(config_str):
            protocol = config_str.split('://')[0].upper()
            logger.info(f"⊘ Skipping {protocol} (not supported by Xray core)")
            return True, 0, config_str
        
        process = None
        config_file = None
        
        try:
            outbound = self.parse_config_string(config_str)
            if not outbound:
                logger.warning(f"✗ Failed to parse config")
                return False, None, config_str
            
            socks_port = find_free_port()
            http_port = find_free_port()
            
            xray_config = self.create_xray_config(outbound, socks_port, http_port)
            
            
            fd, config_file = tempfile.mkstemp(suffix='.json', text=True)
            with os.fdopen(fd, 'w') as f:
                json.dump(xray_config, f)
            
            process = subprocess.Popen(
                [self.xray_path, 'run', '-c', config_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            time.sleep(3)
            
            if process.poll() is not None:
                stderr = process.stderr.read().decode('utf-8', errors='ignore') if process.stderr else ''
                logger.warning(f"✗ Process crashed: {stderr[:100]}")
                return False, None, config_str
            
            proxies = {
                'http': f'http://127.0.0.1:{http_port}',
                'https': f'http://127.0.0.1:{http_port}'
            }
            
            for url in self.test_urls:
                domain = url.split('/')[2]
                start_time = time.time()
                try:
                    response = requests.get(
                        url,
                        proxies=proxies,
                        timeout=self.timeout
                    )
                    delay = int((time.time() - start_time) * 1000)
                    
                    if response.status_code in [200, 204]:
                        logger.info(f"✓ OK ({delay}ms via {domain})")
                        return True, delay, config_str
                    else:
                        logger.warning(f"✗ HTTP {response.status_code} on {domain}")
                        
                except requests.exceptions.ProxyError as e:
                    logger.warning(f"✗ Proxy error: {str(e)}")
                    return False, None, config_str
                except requests.exceptions.Timeout:
                    logger.warning(f"✗ Timeout on {domain}")
                except requests.exceptions.ConnectionError as e:
                    logger.warning(f"✗ Connection error on {domain}: {str(e)}")
                except Exception as e:
                    logger.warning(f"✗ {type(e).__name__} on {domain}: {str(e)}")
            
            logger.warning(f"✗ Failed all test URLs")
            return False, None, config_str
                
        except Exception as e:
            logger.error(f"✗ Setup error: {str(e)}")
            return False, None, config_str
            
        finally:
            if process:
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                        process.wait()
                except:
                    pass
            
            if config_file and os.path.exists(config_file):
                try:
                    os.unlink(config_file)
                except:
                    pass
            
            time.sleep(0.3)


class ParallelXrayTester:
    def __init__(self, xray_path: str = 'xray', max_workers: int = 8, timeout: int = 10, test_urls: List[str] = None):
        self.tester = XrayTester(xray_path, timeout, test_urls)
        self.max_workers = max_workers
        
    def test_all(self, configs: List[str]) -> List[str]:
        logger.info(f"Testing {len(configs)} configs with {self.max_workers} workers...")
        logger.info(f"Test URLs: {self.tester.test_urls}")
        
        working = []
        tested = 0
        skipped = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.tester.test_config, cfg): cfg for cfg in configs}
            
            for future in as_completed(futures):
                config = futures[future]
                tested += 1
                
                
                try:
                    success, delay, config_str = future.result()
                    if success:
                        working.append(config_str)
                        if delay == 0:
                            skipped += 1
                    
                    if tested % 25 == 0:
                        logger.info(f"Progress: {tested}/{len(configs)} ({len(working)} working, {skipped} skipped)")
                
                except Exception as e:
                    logger.error(f"Test error: {str(e)}")
        
        logger.info(f"Results: {len(working)}/{len(configs)} working ({len(working)*100//max(1,len(configs))}%) - {skipped} skipped (unsupported)")
        return working


def main():
    config_settings = ProxyConfig()

    if len(sys.argv) < 3:
        print("Usage: python xray_config_tester.py <input.txt> <output.txt>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not config_settings.ENABLE_XRAY_TESTER:
        logger.info("Xray testing is disabled in user_settings.py. Skipping.")
        try:
            with open(input_file, 'r', encoding='utf-8') as f_in:
                content = f_in.read()
            os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write(content)
            logger.info(f"Copied {input_file} to {output_file} as testing is disabled.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Failed to copy {input_file} to {output_file}: {str(e)}")
            sys.exit(1)

    max_workers = config_settings.XRAY_TESTER_MAX_WORKERS
    timeout = config_settings.XRAY_TESTER_TIMEOUT_SECONDS
    test_urls = config_settings.XRAY_TESTER_URLS
    
    logger.info(f"Loading configs from {input_file}")
    
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    configs = []
    header_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('//') or not line:
            if not configs:
                header_lines.append(line)
        else:
            configs.append(line)
    
    if not configs:
        logger.error("No configs found")
        sys.exit(1)
    
    logger.info(f"Found {len(configs)} configs")
    
    tester = ParallelXrayTester(max_workers=max_workers, timeout=timeout, test_urls=test_urls)
    working = tester.test_all(configs)
    
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for header in header_lines:
            f.write(header + '\n')
        if header_lines:
            f.write('\n')
        for config in working:
            f.write(config + '\n\n')
    
    if working:
        logger.info(f"Saved {len(working)} working configs to {output_file}")
        sys.exit(0)
    else:
        logger.error("No working configs found")
        sys.exit(0)


if __name__ == '__main__':
    main()