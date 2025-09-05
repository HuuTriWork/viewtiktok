import os, sys, time, json, requests

TOKEN_FILE = "api_token.txt"
DELAY_SECONDS = 180

try:
    from colorama import init as _cinit, Fore, Style
    _cinit(autoreset=True)
except Exception:
    class _F:
        RED="\033[31m"; GREEN="\033[32m"; YELLOW="\033[33m"; CYAN="\033[36m"; MAGENTA="\033[35m"
        RESET="\033[0m"; BRIGHT="\033[1m"
    class _S: RESET_ALL="\033[0m"
    Fore=_F(); Style=_S()

def _input_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            t = f.read().strip()
            if t:
                return t
    t = input(f"{Fore.CYAN}{Style.BRIGHT}Nhập API token: {Style.RESET_ALL}").strip()
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(t)
    return t

def _spinner_wait(seconds):
    marks = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for i in range(seconds):
        s = marks[i % len(marks)]
        remain = seconds - i
        mm, ss = divmod(remain, 60)
        sys.stdout.write(
            f"\r{Fore.YELLOW}{Style.BRIGHT}{s} Đang delay, thử lại sau {mm:02d}:{ss:02d}...{Style.RESET_ALL}"
        )
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

def _post_order(token, url, data):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
        "Origin": "https://like.vn",
        "Referer": "https://like.vn/",
        "api-token": token
    }
    r = requests.post(url, headers=headers, data=data, timeout=30)
    try:
        return r.status_code, r.json()
    except Exception:
        return r.status_code, {"status":"error","message":"Phản hồi không phải JSON"}

def main():
    print(Fore.MAGENTA + Style.BRIGHT + """
══════════════════════════════════════
             MENU TOOLS
══════════════════════════════════════
 [1] View TikTok         (1000 view)
 [2] Like TikTok         (10 like)
 [3] Follow TikTok       (10 follow)
 [4] Like Fanpage FB     (10 like)
 [5] Like Instagram      (10 like)
══════════════════════════════════════
""" + Style.RESET_ALL)

    choice = input(Fore.YELLOW + "👉 Chọn dịch vụ (1-5): " + Style.RESET_ALL).strip()
    link = input(Fore.CYAN + "🔗 Nhập link: " + Style.RESET_ALL).strip()
    token = _input_token()

    if choice == "1":
        url = "https://like.vn/api/mua-view-tiktok/order"
        data = {"objectId": link, "server_order": "4", "giftcode": "", "amount": "1000", "note": ""}
    elif choice == "2":
        url = "https://like.vn/api/mua-like-tiktok/order"
        data = {"objectId": link, "server_order": "6", "giftcode": "", "amount": "10", "note": ""}
    elif choice == "3":
        url = "https://like.vn/api/mua-follow-tiktok/order"
        data = {"objectId": link, "server_order": "5", "giftcode": "", "amount": "10", "note": ""}
    elif choice == "4":
        url = "https://like.vn/api/mua-like-fanpage-facebook/order"
        data = {"objectId": link, "server_order": "6", "giftcode": "", "amount": "10", "note": ""}
    elif choice == "5":
        url = "https://like.vn/api/mua-like-instagram/order"
        data = {"objectId": link, "server_order": "6", "giftcode": "", "amount": "10", "note": ""}
    else:
        print(Fore.RED + "❌ Lựa chọn không hợp lệ!")
        return

    announced_delay = False
    while True:
        status_code, result = _post_order(token, url, data)
        if status_code != 200:
            print(f"{Fore.YELLOW}{Style.BRIGHT}⏳ Đang delay...{Style.RESET_ALL}")
            _spinner_wait(DELAY_SECONDS)
            continue

        status = str(result.get("status", "")).lower()
        message = result.get("message", "")

        if status == "success" and "Lên đơn thành công" in message:
            print(f"{Fore.GREEN}{Style.BRIGHT}✅ Thành công!{Style.RESET_ALL}")
            announced_delay = False
            _spinner_wait(DELAY_SECONDS)
            continue

        if status == "error" and "miễn phí" in message:
            if not announced_delay:
                print(f"{Fore.YELLOW}{Style.BRIGHT}⏳ Đang delay.{Style.RESET_ALL}")
                announced_delay = True
            _spinner_wait(DELAY_SECONDS)
            continue

        if status == "error":
            print(f"{Fore.YELLOW}{Style.BRIGHT}⏳ Đang delay...{Style.RESET_ALL}")
            _spinner_wait(DELAY_SECONDS)
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}⏹ Đã dừng bởi người dùng.{Style.RESET_ALL}")
