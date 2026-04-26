import requests
import json

def run_opsec_audit():
    print("[!] Memulai Audit OPSEC Jaringan...")
    
    PROXY_URL = "" 
    
    proxies = {
        "http": PROXY_URL,
        "https": PROXY_URL
    } if PROXY_URL else None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }

    try:
        print("[!] Menghubungi Echo Server...")
        res = requests.get("https://httpbin.org/anything", headers=headers, proxies=proxies, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            
            print("\n[*] --- HASIL AUDIT IDENTITAS ---")
            print(f"[+] IP Terbaca oleh Server : {data.get('origin')}")
            
            print("\n[*] --- HEADERS YANG BOCOR ---")
            for key, val in data.get('headers', {}).items():
                print(f" - {key}: {val}")
                
            print("\n[*] --- ANALISIS KEBOCORAN ---")
            if "X-Forwarded-For" in data.get('headers', {}) or "Via" in data.get('headers', {}):
                print("[-] PERINGATAN BENDERA MERAH: Proxy kamu membocorkan identitas (Transparent Proxy).")
            else:
                print("[+] OPSEC BERSIH: Tidak ada jejak routing proxy yang terdeteksi.")
        else:
            print(f"[-] Gagal mendapatkan respon. Status: {res.status_code}")

    except Exception as e:
        print(f"[!] Error pada eksekusi: {e}")

if __name__ == "__main__":
    run_opsec_audit()