import time

class WAFTokenBucket:
    def __init__(self, ip_address, max_burst, refill_rate):
        self.ip = ip_address
        self.max_burst = max_burst
        self.tokens = max_burst
        self.refill_rate = refill_rate
        self.last_check = time.time()

    def process_request(self):
        now = time.time()
        time_passed = now - self.last_check
        self.tokens += time_passed * self.refill_rate
        
        if self.tokens > self.max_burst:
            self.tokens = self.max_burst
            
        self.last_check = now

        if self.tokens >= 1:
            self.tokens -= 1
            return 200 
        else:
            return 429 

def simulate_attack_on_waf():
    target_waf = WAFTokenBucket(ip_address="114.10.42.93", max_burst=15, refill_rate=5)
    
    print("[!] WAF Aktif. Menerima serangan asimetris...")
    
    for i in range(1, 31):
        status = target_waf.process_request()
        if status == 200:
            print(f"Request {i}: [200 OK] -> Tembus")
        else:
            print(f"Request {i}: [429/403 DROP] -> IP Diblokir WAF")
        
        time.sleep(0.1)

if __name__ == "__main__":
    simulate_attack_on_waf()