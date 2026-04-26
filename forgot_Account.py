import requests
from bs4 import BeautifulSoup

def execute_probe(u):
    b = "https://team77-theslot777.lol"
    r = f"{b}/Account/ForgotPassword"
    s = requests.Session()
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': r,
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        t_req = s.get(r, headers=h)
        soup = BeautifulSoup(t_req.text, 'html.parser')
        token = soup.find('input', {'name': '__RequestVerificationToken'})
        if not token:
            print("TOKEN_NOT_FOUND")
            return
        p = {
            '__RequestVerificationToken': token['value'],
            'EmailOrUsername': u,
            'Step': '1'
        }
        res = s.post(r, data=p, headers=h)
        print(f"STATUS: {res.status_code}")
        print(f"BODY: {res.text[:2000]}")
    except Exception as e:
        print(f"ERR: {e}")

if __name__ == "__main__":
    execute_probe("bochboch")