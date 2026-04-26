import requests
import time
import random

def shadow_map(target_url):
    print(f"[!] Shadow mapping for: {target_url}")

    paths = [
        "/web.config", "/bin/", "/api/v1/", "/admin/", "/account/Login", "Member/Login", "/App_Data/", "/setup.php", "/.env", "/config", "/api/user/get", "/api/account/status", "/scripts/", "/backup/", "/.git/", "/.svn/", "/.htaccess", "/.htpasswd", "/.DS_Store", "/.well-known/", "/server-status", "/phpinfo.php", "/test.php", "/debug/", "/logs/", "/tmp/", "/old/", "/dev/", "/staging/", "/backup/", "/database/", "/db/", "/data/", "/private/", "/secret/", "/hidden/", "/config.php", "/config.json", "/config.yaml", "/config.yml", "/.env", "/.env.local", "/.env.production", "/.env.development", "/.env.testing", "/.env.staging, /user/login", "/user/register", "/api/auth/login", "/api/auth/register", "/api/v1/auth/login", "/api/v1/auth/register"
    ]

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'referrer': target_url
    }

    for path in paths:
        url = f"{target_url.rstrip('/')}{path}"
        try:
            time.sleep(random.uniform(1, 3))
            response = requests.head(url, headers=headers, timeout=5, allow_redirects=False)
            status = response.status_code
            if status == 200:
                print(f"[+] FOUND (200): {url} - open access")
            elif status == 403:
                print(f"[-] FOUND (403): {url} - WAF Detected Permission.")
            elif status == 302 or status == 301:
                print(f"[/] REDIRECT ({status}): {url} -> {response.headers.get('Location')}")
        except Exception as e:
            print(f"[!] Error checking {url}: {e}")
    
if __name__ == "__main__":
    base_url = "https://team77-theslot777.lol/"
    shadow_map(base_url)