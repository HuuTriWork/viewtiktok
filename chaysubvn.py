import os
import time
import requests
from colorama import init, Fore

init(autoreset=True)

API_URL = "https://chaysub.vn/api/v1/order"
TOKEN_FILE = "api_token.txt"

def get_api_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        os.system("cls" if os.name == "nt" else "clear")
        token = input(Fore.CYAN + "🔑 Nhập API Token: ").strip()
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(token)
        return token

def create_order(object_id, api_token):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://chaysub.vn",
        "Referer": "https://chaysub.vn/service/free/free"
    }

    data = {
        "object_id": object_id,
        "provider_server": "34225",
        "quantity": "500",
        "schedule_date": "",
        "schedule_time": "",
        "repeat_interval": "1",
        "repeat_delay": "0",
        "note": ""
    }

    try:
        resp = requests.post(API_URL, headers=headers, data=data, timeout=30)
        return resp.status_code, resp.json()
    except Exception as e:
        return 500, {"status": "error", "message": str(e)}

def countdown(sec):
    while sec > 0:
        m, s = divmod(sec, 60)
        print(f"\r{Fore.YELLOW}⏳ Đang delay: {m:02d}:{s:02d}", end="")
        time.sleep(1)
        sec -= 1
    print("\r", end="")

if __name__ == "__main__":
    api_token = get_api_token()
    os.system("cls" if os.name == "nt" else "clear")
    object_id = input(Fore.CYAN + "🔗 Nhập link: ").strip()

    while True:
        status, result = create_order(object_id, api_token)

        if status == 200 and result.get("status") == "success":
            print(Fore.GREEN + f"✅ Đã tăng 500 view | Mã đơn: {result['data']['order_code']}")
        else:
            print(Fore.YELLOW + "⚠️ Đơn trước chưa hoàn thành, vui lòng thử lại sau...")

        countdown(30)
