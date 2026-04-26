import requests
import json
def analyze_target(url):
    print(f"[!] Analyzing target: {url}")
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        print("\n[*] Response")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
                  
            print("\n[*] Security")
            server = response.headers.get('Server', 'Unknown')
            if 'cloudflare' in server.lower() or 'cf-ray' in response.headers:
                print("Cloudflare detected")
            elif 'litespeed' in server.lower():
                print("No Cloudflare detected")
            else:
                print(f"[+] Server: {server}")

            set_cookie = response.headers.get('Set-Cookie', '')
            if "HttpOnly" in set_cookie:
                print("[+] HttpOnly cookie detected")
            else:
                print("[-] No HttpOnly cookie detected")

    except Exception as e:
        print(f"Error analyzing target: {e}")

if __name__ == "__main__":
    target_url = "https://team77-theslot777.lol/home?login"
    analyze_target(target_url)