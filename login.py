import requests
from bs4 import BeautifulSoup

def simulate_login(username, password):
    base_url = "https://team77-theslot777.lol"
    login_url = f"{base_url}/home?login"
    post_url = f"{base_url}/Account/Login"

    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': login_url
    }

    try:
        print(f"[!] CSRF Token from {login_url}...")
        response = session.get(login_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        token = soup.find('input', {'name': '__RequestVerificationToken'})
        if not token:
            print("[-] CSRF token not found.")
            return
        
        token_value = token['value']
        print(f"[+] Token saya dapat. hahahaaa mampuss lu: {token_value[:15]}...")

        payload = {
            '__RequestVerificationToken': token_value,
            'Username': username,
            'Password': password,
            'RememberMe': 'false'
        }

        print(f"\n[*] Send payload ke {post_url}...")
        post_response = session.post(post_url, data=payload, headers=headers, allow_redirects=False
        )

        print(f"[*] Server Response")
        print(f"Status Code: {post_response.status_code}")
        print(f"Headers: {dict(post_response.headers)}")

        if "Object moved" in post_response.text or post_response.status_code in [301, 302]:
            print("[+] Login successful! Redirect detected.")
        else:
            print(f"[-] Login failed. Response content:\n{post_response.text[:500]}")

    except Exception as e:
        print(f"[!] Error babi: {e}")

if __name__ == "__main__":
    my_user = "bochboch"
    my_pass = "Make1tright!"
    simulate_login(my_user, my_pass)
