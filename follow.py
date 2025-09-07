import sys
import subprocess
import importlib
import requests
import time
import itertools
import os

def install_if_missing(package):
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for module in ["requests"]:
    install_if_missing(module)

success_count = 0
total_follow = 0
TOKEN_FILE = "api_token.txt"

def get_api_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token = f.read().strip()
        if token:
            return token
    token = input("Nhập API Token (lấy tại https://like.vn/docs/api): ").strip()
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    return token

def send_request(url, headers, payload):
    try:
        r = requests.post(url, headers=headers, data=payload)
        return r.json()
    except:
        return {"status": "error"}

def animate_in_progress(success, total, duration=120):
    dots = itertools.cycle(["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"])
    start = time.time()
    while time.time() - start < duration:
        sys.stdout.write(f"\rStatus: In progress {next(dots)} | Success: {success} | Total Follow: {total}")
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write("\r")
    sys.stdout.flush()

def order_follow(link):
    global success_count, total_follow

    api_token = get_api_token()
    url = "https://like.vn/api/mua-follow-tiktok/order"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "api-token": api_token,
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "origin": "https://like.vn",
        "referer": "https://like.vn/mua-follow-tiktok",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "x-requested-with": "XMLHttpRequest"
    }

    payload = {
        "objectId": link,
        "server_order": 5,
        "giftcode": "",
        "amount": 10,
        "note": ""
    }

    while True:
        sys.stdout.write(f"\rStatus: Order | Success: {success_count} | Total Follow: {total_follow}  ")
        sys.stdout.flush()
        data = send_request(url, headers, payload)

        if data.get("status") == "success":
            success_count += 1
            total_follow += 10

        animate_in_progress(success_count, total_follow, duration=120)

        if data.get("status") in ["success", "error"]:
            continue
        else:
            break

if __name__ == "__main__":
    try:
        link = input("Nhập Link Profile Tiktok (dạng https://www.tiktok.com/@username): ").strip()
        while True:
            order_follow(link)
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
