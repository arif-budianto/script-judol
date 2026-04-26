import asyncio
import aiohttp
import sys

async def check_proxy(session, proxy, valid_proxies):
    url = "http://httpbin.org/ip"
    proxy_url = f"http://{proxy}"
    
    try:
        async with session.get(url, proxy=proxy_url, timeout=3) as response:
            if response.status == 200:
                data = await response.json()
                print(f"[+] {proxy} | {data.get('origin', 'Unknown')}")
                valid_proxies.append(proxy)
            else:
                print(f"[-] {proxy} | {response.status}")
    except Exception:
        print(f"[!] {proxy} | RTO")

async def run_validator():
    try:
        with open("raw_proxies.txt", "r") as f:
            raw_proxies =[line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[X] File raw_proxies.txt tidak ditemukan.")
        sys.exit(1)

    if not raw_proxies:
        print("[X] File raw_proxies.txt kosong. Isi dengan IP:PORT.")
        sys.exit(1)

    print(f"[>] Memulai validasi {len(raw_proxies)} node...")
    valid_proxies =[]
    
    async with aiohttp.ClientSession() as session:
        tasks = [check_proxy(session, proxy, valid_proxies) for proxy in raw_proxies]
        await asyncio.gather(*tasks)

    print(f"[>] Selesai. {len(valid_proxies)} proxy hidup disimpan ke live_proxies.txt")
    with open("live_proxies.txt", "w") as f:
        for p in valid_proxies:
            f.write(f"{p}\n")

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_validator())