import time
import requests
from datetime import datetime
import sys

# =====================================================================
# 🔑 CONFIGURATION (သင့်ရဲ့ Token များကို ဒီနေရာမှာ ထည့်သွင်းပါ)
# =====================================================================
# ၁။ ဂိမ်းဆွဲမယ့် API Bearer Token
GAME_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzc5NjczNTAxIiwibmJmIjoiMTc3OTY3MzUwMSIsImV4cCI6IjE3Nzk2NzUzMDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRလွှမ်းမိုးမှုရှိသောလော့ထရီတိုကင်"

# ၂။ Telegram BotFather ဆီကရတဲ့ Bot Token
TELEGRAM_BOT_TOKEN = "8732215456:AAGLCJXwTqBV9cIqusCnm7x0OhnPLsi0TU0"

# ၃။ သင့်ရဲ့ Telegram User ID (သို့မဟုတ်) Channel Username (ဥပမာ- "@my_channel")
TELEGRAM_CHAT_ID = "8193986737"
# =====================================================================

GAME_URL = "https://ckygjf6r.com/api/webapi/GetNoaverageEmerdList"
session = requests.Session()

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

# နောက်ဆုံးထွက်ထားတဲ့ ပွဲစဉ် (Issue Number) ကို မှတ်ထားဖို့ Variable
last_checked_issue = None

def send_telegram_message(text):
    """ Telegram Chat/Channel ထံသို့ စာသားလှမ်းပို့ပေးသည့် Function """
    tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown" # စာသားတွေကို အမည်းရောင်၊ စောင်းရောင် စတိုင်ဖော်လို့ရအောင်
    }
    try:
        res = requests.post(tg_url, json=payload, timeout=10)
        if res.status_code == 200:
            print(f"{Colors.GREEN}[✓] Telegram သို့ Message ပို့ပြီးပါပြီ။{Colors.END}", flush=True)
        else:
            print(f"{Colors.RED}[-] Telegram Send Failed: {res.text}{Colors.END}", flush=True)
    except Exception as e:
        print(f"{Colors.RED}[-] Telegram Connection Error: {e}{Colors.END}", flush=True)

def fetch_data():
    global last_checked_issue
    current_timestamp = int(time.time())
    
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {GAME_API_TOKEN}" if not GAME_API_TOKEN.startswith("Bearer ") else GAME_API_TOKEN,
        "Ar-Origin": "https://www.cklottery.top",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    payload = {
        "pageSize": 1, # Telegram ထဲ ရှုပ်မနေအောင် နောက်ဆုံးထွက်တဲ့ ၁ ကြိမ်စာပဲ ဖတ်မယ်
        "pageNo": 1,
        "typeId": 30,
        "language": 0,
        "random": "be8d0ae92c154507a735d86a2d792cd3",
        "signature": "DBDC04A4BEB3AAAB575F34FD0B4C6872",
        "timestamp": current_timestamp
    }

    try:
        response = session.post(GAME_URL, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0 and "data" in result:
                game_list = result["data"].get("list", [])
                
                if game_list:
                    latest_game = game_list[0]
                    issue = latest_game.get("issueNumber", "N/A")
                    num = latest_game.get("number", "N/A")
                    colour = latest_game.get("colour", "N/A").upper()
                    premium = latest_game.get("premium", "N/A")
                    server_time = result.get('serviceNowTime', 'Unknown')

                    # ပွဲစဉ်အသစ် ထွက်လာမှသာ Telegram ကို ပို့ပေးမည့် စနစ် (Message ထပ်မနေအောင်)
                    if issue != last_checked_issue:
                        last_checked_issue = issue
                        
                        # ရလဒ်အလိုက် အလှဆင်မည့် Emoji ရွေးချယ်ခြင်း
                        emoji = "🟢" if "GREEN" in colour else "🔴" if "RED" in colour else "🟣"
                        if "VIOLET" in colour and ("RED" in colour or "GREEN" in colour):
                            emoji = "🔮"

                        # Telegram ထဲသို့ ရောက်မည့် စတိုင်မိုက် Markdown စာသား ပုံစံ
                        tg_text = (
                            f"🎰 *30S LOTTERY RESULT* 🎰\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🆔 *Issue:* `{issue}`\n"
                            f"🔢 *Number:* `{num}`\n"
                            f"🎨 *Colour:* {emoji} `{colour}`\n"
                            f"💰 *Premium:* `{premium}`\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🕒 *Time:* `{server_time}`"
                        )
                        
                        # Terminal Log မှာ ပြသခြင်း
                        print(f"{Colors.BOLD}{Colors.CYAN}\n[+] New Result Detected ({issue})! Sending to Telegram...{Colors.END}", flush=True)
                        
                        # Telegram သို့ လှမ်းပို့ခြင်း
                        send_telegram_message(tg_text)
                    else:
                        print(".", end="", flush=True) # ပွဲစဉ်အသစ်မရှိသေးရင် အစက်လေးတွေပဲ ပြနေမယ်
            else:
                print(f"\n{Colors.RED}[-] API Alert: {result.get('msg')}{Colors.END}", flush=True)
        else:
            print(f"\n{Colors.RED}[-] HTTP Error: Code {response.status_code}{Colors.END}", flush=True)
            
    except Exception as e:
        print(f"\n{Colors.RED}[-] Network Error: {e}{Colors.END}", flush=True)

if __name__ == "__main__":
    print(f"{Colors.BOLD}{Colors.GREEN}[*] 🟢 System Online with Telegram Gateway Enabled!{Colors.END}", flush=True)
    print("[*] Waiting for new lottery rounds...", flush=True)
    
    while True:
        fetch_data()
        time.sleep(5) # API ကို ၅ စက္ကန့်တစ်ခါ Live စစ်ပြီး ပွဲသစ်ထွက်တာနဲ့ တန်းဖတ်မည်
