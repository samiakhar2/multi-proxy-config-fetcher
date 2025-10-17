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
from contextlib import closing

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class SingBoxTester:
    def __init__(self, singbox_path: str = 'sing-box', timeout: int = 10):
        self.singbox_path = singbox_path
        self.timeout = timeout
        self.test_url = 'https://www.youtube.com/generate_204'
        
    def create_minimal_config(self, outbound: Dict, mixed_port: int) -> Dict:
        return {
            "log": {
                "level": "panic",
                "timestamp": False
            },
            "inbounds": [
                {
                    "type": "mixed",
                    "listen": "127.0.0.1",
                    "listen_port": mixed_port
                }
            ],
            "outbounds": [outbound],
            "route": {
                "final": outbound.get('tag', 'proxy')
            }
        }
    
    def test_config(self, outbound: Dict) -> Tuple[bool, Optional[int], str]:
        tag = outbound.get('tag', 'unknown')
        mixed_port = find_free_port()
        process = None
        config_file = None
        
        try:
            config = self.create_minimal_config(outbound, mixed_port)
            
            fd, config_file = tempfile.mkstemp(suffix='.json', text=True)
            with os.fdopen(fd, 'w') as f:
                json.dump(config, f)
            
            process = subprocess.Popen(
                [self.singbox_path, 'run', '-c', config_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            time.sleep(3)
            
            if process.poll() is not None:
                stderr = process.stderr.read().decode('utf-8', errors='ignore') if process.stderr else ''
                logger.warning(f"✗ {tag} - Process crashed: {stderr[:100]}")
                return False, None, tag
            
            start_time = time.time()
            
            try:
                response = requests.get(
                    self.test_url,
                    proxies={
                        'http': f'http://127.0.0.1:{mixed_port}',
                        'https': f'http://127.0.0.1:{mixed_port}'
                    },
                    timeout=self.timeout
                )
                
                delay = int((time.time() - start_time) * 1000)
                
                if response.status_code in [200, 204]:
                    logger.info(f"✓ {tag} - OK ({delay}ms)")
                    return True, delay, tag
                else:
                    logger.warning(f"✗ {tag} - HTTP {response.status_code}")
                    return False, None, tag
                    
            except requests.exceptions.ProxyError:
                logger.warning(f"✗ {tag} - Proxy error")
                return False, None, tag
            except requests.exceptions.Timeout:
                logger.warning(f"✗ {tag} - Timeout")
                return False, None, tag
            except requests.exceptions.ConnectionError:
                logger.warning(f"✗ {tag} - Connection error")
                return False, None, tag
            except Exception as e:
                logger.warning(f"✗ {tag} - {type(e).__name__}")
                return False, None, tag
                
        except Exception as e:
            logger.error(f"✗ {tag} - Setup error: {str(e)}")
            return False, None, tag
            
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


class ParallelConfigTester:
    def __init__(self, singbox_path: str = 'sing-box', max_workers: int = 8, timeout: int = 10):
        self.tester = SingBoxTester(singbox_path, timeout)
        self.max_workers = max_workers
        
    def test_all(self, outbounds: List[Dict]) -> List[Dict]:
        logger.info(f"Testing {len(outbounds)} configs with {self.max_workers} workers...")
        logger.info(f"Test URL: {self.tester.test_url}")
        
        working = []
        tested = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.tester.test_config, ob): ob for ob in outbounds}
            
            for future in as_completed(futures):
                outbound = futures[future]
                tested += 1
                
                try:
                    success, delay, tag = future.result()
                    if success and delay is not None:
                        outbound['_test_delay'] = delay
                        working.append(outbound)
                    
                    if tested % 25 == 0:
                        logger.info(f"Progress: {tested}/{len(outbounds)} ({len(working)} working)")
                        
                except Exception as e:
                    logger.error(f"Test error: {str(e)}")
        
        working.sort(key=lambda x: x.get('_test_delay', 999999))
        
        for ob in working:
            ob.pop('_test_delay', None)
        
        logger.info(f"Results: {len(working)}/{len(outbounds)} working ({len(working)*100//max(1,len(outbounds))}%)")
        return working


def update_config_with_working_outbounds(config: Dict, working_outbounds: List[Dict]) -> Dict:
    if not working_outbounds:
        logger.warning("No working outbounds - keeping original config")
        return config
    
    working_tags = {ob['tag'] for ob in working_outbounds}
    
    new_outbounds = []
    
    for ob in config['outbounds']:
        ob_type = ob.get('type')
        
        if ob_type == 'selector':
            new_list = []
            for tag in ob.get('outbounds', []):
                if tag in working_tags or tag in ['👽 Best Ping 🚀', 'auto', 'direct', 'block']:
                    new_list.append(tag)
            ob['outbounds'] = new_list
            new_outbounds.append(ob)
            
        elif ob_type == 'urltest':
            new_list = [tag for tag in ob.get('outbounds', []) if tag in working_tags]
            if new_list:
                ob['outbounds'] = new_list
                new_outbounds.append(ob)
            
        elif ob_type in ['direct', 'block', 'dns']:
            new_outbounds.append(ob)
            
        elif ob.get('tag') in working_tags:
            new_outbounds.append(ob)
    
    config['outbounds'] = new_outbounds
    return config


def main():
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python config_tester.py <input.json> <output.json> [max_workers] [timeout]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    max_workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    timeout = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    
    logger.info(f"Loading config from {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    proxy_outbounds = [
        ob for ob in config.get('outbounds', [])
        if ob.get('type') not in ['selector', 'urltest', 'direct', 'block', 'dns']
    ]
    
    if not proxy_outbounds:
        logger.error("No proxy outbounds found")
        sys.exit(1)
    
    logger.info(f"Found {len(proxy_outbounds)} proxy outbounds")
    
    tester = ParallelConfigTester(max_workers=max_workers, timeout=timeout)
    working = tester.test_all(proxy_outbounds)
    
    if working:
        config = update_config_with_working_outbounds(config, working)
        
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        logger.info(f"Saved {len(working)} working configs to {output_file}")
        sys.exit(0)
    else:
        logger.error("No working configs found")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        sys.exit(0)


if __name__ == '__main__':
    main()