import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_api_from_js(target_url):
    print(f"[!] Inteligence Boch is Here. Bochboch: {target_url}")
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        res = requests.get(target_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        js_files = [urljoin(target_url, script['src']) for script in soup.find_all('script') if script.get('src')]

        print(f"[*] Found {len(js_files)} JavaScript files.")

        pattern = r'["\'](/a-zA-Z0-9_\-/]+)["\']'

        found_endpoints = set()

        for js_url in js_files:
            print(f"[ ] Scanning: {js_url}")
            js_res = requests.get(js_url, headers=headers, timeout=10)
            matches = re.findall(pattern, js_res.text)
            for m in matches:
                if len(m) > 3 and '/' in m:
                    found_endpoints.add(m)
        
        print("\n[+] Real Endpoints")
        for ep in sorted(found_endpoints):
            if any(x in ep.lower() for x in ['api', 'login', 'account', 'auth', 'user', 'status', 'verify', 'data', 'info']):
                print(f"[!] Potential Entry: {target_url.rstrip('/')}{ep}")
            else:
                print(f"[-] Path: {ep}")
        
    except Exception as e:
        print(f"Error extracting API endpoints: {e}")

if __name__ == "__main__":
    target = "https://team77-theslot777.lol"
    extract_api_from_js(target)