import os
import sys
import time
import json
import requests

TOKEN_FILE = "token.txt"
URL = "https://like.vn/api/mua-view-tiktok/order"
DELAY_SECONDS = 180

try:
    from colorama import init as _cinit, Fore, Style
    _cinit(autoreset=True)
except Exception:
    class _F: RED="\033[31m"; GREEN="\033[32m"; YELLOW="\033[33m"; CYAN="\033[36m"; RESET="\033[0m"; BRIGHT="\033[1m"
    class _S: RESET_ALL="\033[0m"
    Fore=_F(); Style=_S()

def _input_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            t = f.read().strip()
            if t: return t
    t = input(f"{Fore.CYAN}{Style.BRIGHT}Nhập API token: {Style.RESET_ALL}").strip()
    with open(TOKEN_FILE, "w", encoding="utf-8") as f: f.write(t)
    return t

def _spinner_wait(seconds):
    marks = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for i in range(seconds):
        s = marks[i % len(marks)]
        remain = seconds - i
        mm, ss = divmod(remain, 60)
        sys.stdout.write(f"\r{Fore.YELLOW}{Style.BRIGHT}{s} Đang delay, thử lại sau {mm:02d}:{ss:02d}...{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 70 + "\r")
    sys.stdout.flush()

def _post_order(token, link, amount="1000", server_order="4", giftcode="", note=""):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
        "Origin": "https://like.vn",
        "Referer": "https://like.vn/mua-view-tiktok",
        "api-token": token
    }
    data = {"objectId": link, "server_order": server_order, "giftcode": giftcode, "amount": amount, "note": note}
    r = requests.post(URL, headers=headers, data=data, timeout=30)
    try:
        return r.status_code, r.json()
    except Exception:
        return r.status_code, {"status":"error","message":f"Phản hồi không phải JSON: {r.text[:200]}..."}

def main():
    api_token = _input_token()
    link = input(f"{Fore.CYAN}{Style.BRIGHT}Nhập link TikTok: {Style.RESET_ALL}").strip()
    announced_delay = False
    while True:
        status_code, result = _post_order(api_token, link)
        if status_code != 200:
            print(f"{Fore.RED}{Style.BRIGHT}HTTP {status_code}{Style.RESET_ALL} | {json.dumps(result, ensure_ascii=False)}")
            break

        status = str(result.get("status", "")).lower()
        message = result.get("message", "")

        if status == "success" and "Lên đơn thành công" in message:
            print(f"{Fore.GREEN}{Style.BRIGHT}✅ Thành công:{Style.RESET_ALL} {json.dumps(result, ensure_ascii=False)}")
            announced_delay = False
            _spinner_wait(DELAY_SECONDS)
            continue

        if status == "error" and "miễn phí" in message:
            if not announced_delay:
                print(f"{Fore.YELLOW}{Style.BRIGHT}⏳ Đang delay (đang có đơn miễn phí chạy).{Style.RESET_ALL}")
                announced_delay = True
            _spinner_wait(DELAY_SECONDS)
            continue

        print(f"{Fore.RED}{Style.BRIGHT}❌ Lỗi:{Style.RESET_ALL} {json.dumps(result, ensure_ascii=False)}")
        break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Đã dừng bởi người dùng.{Style.RESET_ALL}")
