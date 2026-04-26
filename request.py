import argparse
import sys
import webbrowser

import requests

DEFAULT_TARGET_URL = "https://team77-theslot777.lol/home?login"
DEFAULT_TIMEOUT_SECONDS = 15

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
}


def check_url_access(target_url: str, timeout_seconds: int) -> bool:
    try:
        response = requests.get(
            target_url,
            headers=HEADERS,
            timeout=timeout_seconds,
            allow_redirects=True,
        )
    except requests.RequestException as error:
        print(f"Gagal mengakses URL: {error}")
        return False

    print(f"URL final: {response.url}")
    print(f"Status: {response.status_code}")

    if response.ok:
        print("Berhasil diakses.")
        return True

    print("URL merespons, tapi statusnya bukan sukses.")
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cek akses URL dan opsional buka di browser.")
    parser.add_argument(
        "url",
        nargs="?",
        default=DEFAULT_TARGET_URL,
        help=f"URL yang dicek. Default: {DEFAULT_TARGET_URL}",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Buka URL di browser default setelah pengecekan berhasil.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Timeout request dalam detik. Default: {DEFAULT_TIMEOUT_SECONDS}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    is_accessible = check_url_access(args.url, args.timeout)
    if is_accessible and args.open:
        webbrowser.open(args.url)

    return 0 if is_accessible else 1


if __name__ == "__main__":
    sys.exit(main())
