import time
import concurrent.futures

class WAFMultiNode:
    def __init__(self, max_burst, refill_rate):
        self.max_burst = max_burst
        self.refill_rate = refill_rate
        self.ip_buckets = {}

    def _get_bucket(self, ip):
        if ip not in self.ip_buckets:
            self.ip_buckets[ip] = {
                'tokens': self.max_burst,
                'last_check': time.time()
            }
        return self.ip_buckets[ip]

    def process_request(self, ip):
        now = time.time()
        bucket = self._get_bucket(ip)
        
        time_passed = now - bucket['last_check']
        bucket['tokens'] += time_passed * self.refill_rate
        
        if bucket['tokens'] > self.max_burst:
            bucket['tokens'] = self.max_burst
            
        bucket['last_check'] = now

        if bucket['tokens'] >= 1:
            bucket['tokens'] -= 1
            return 200
        else:
            return 429

def attack_worker(waf, ip, req_id):
    status = waf.process_request(ip)
    if status == 200:
        print(f"[*] Node {ip} | Req {req_id}:[200 OK] -> Tembus")
    else:
        print(f"[!] Node {ip} | Req {req_id}:[429 DROP] -> Limit Tercapai")

def run_distributed_simulation():
    target_waf = WAFMultiNode(max_burst=5, refill_rate=1)
    
    proxy_pool =[
        "192.168.1.10",
        "192.168.1.11",
        "192.168.1.12",
        "192.168.1.13",
        "192.168.1.14"
    ]
    
    print("[>] Menginisiasi Serangan Terdistribusi (Rotasi 5 Node)...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures =[]
        for i in range(1, 41):
            current_ip = proxy_pool[i % len(proxy_pool)]
            futures.append(executor.submit(attack_worker, target_waf, current_ip, i))
            time.sleep(0.05)
            
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    run_distributed_simulation()
    