import time
import requests
from datetime import datetime
import sys

# =====================================================================
# 🔑 CONFIGURATION SETTINGS (ဒီနေရာမှာ သင့် Token များကို အစားထိုးပါ)
# =====================================================================
# ၁။ ဂိမ်းဆွဲမယ့် API ရဲ့ Bearer Token (လက်ရှိ ပေးထားသော Token အဟောင်း)
GAME_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzc5NjczNTAxIiwibmJmIjoiMTc3OTY3MzUwMSIsImV4cCI6IjE3Nzk2NzUzMDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI1LzI1LzIwMjYgODo0NTowMSBBTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjQ4NzIwMyIsIlVzZXJOYW1lIjoiOTU5Nzc3NTQ1NTg5IiwiVXNlclBob3RvIjoiMjAiLCJOaWNrTmFtZSI6Ik1HVEhBTlQgIiwiQW1vdW50IjoiMi42MSIsIkludGVncmFsIjoiMCIsIkxvZ2luTWFyayI6Ikg1IiwiTG9naW5UaW1lIjoiNS8yNS8yMDI2IDg6MTU6MDEgQU0iLCJMb2dpbklQQWRkcmVzcyI6IjExNi4yMDYuMTkzLjQwIiwiRGJOdW1iZXIiOiIwIiwiSXN2YWxpZGF0b3IiOiIwIiwiS2V5Q29kZSI6IjYwNSIsIlRva2VuVHlwZSI6IkFjY2Vzc19Ub2tlbiIsIlBob25lVHlwZSI6IjEiLCJVc2VyVHlwZSI6IjAiLCJVc2VyTmFtZTIiOiIiLCJpc3MiOiJqd3RJc3N1ZXIiLCJhdWQiOiJsb3R0ZXJ5VGlja2V0In0.x3qj70HmHJKnSsYTI08LqurJ-KB4W7e0syYMwPWfbvE"

# ၂။ Telegram BotFather ထံမှ ရရှိလာသော Bot Token
TELEGRAM_BOT_TOKEN = "8732215456:AAGLCJXwTqBV9cIqusCnm7x0OhnPLsi0TU0"

# ၃။ သင့် Telegram Channel Name (ဥပမာ- "@my_channel") သို့မဟုတ် User ID (ဥပမာ- "12345678")
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

# နောက်ဆုံး ထွက်ထားတဲ့ ပွဲစဉ်နံပါတ်ကို မှတ်ထားမယ့် Variable
last_checked_issue = None

def send_telegram_signal(text):
    """ Telegram Chat သို့မဟုတ် Channel ထံသို့ သန့်ရှင်းလှပသော Message ပို့ပေးသည့် Function """
    tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        res = session.post(tg_url, json=payload, timeout=12)
        if res.status_code == 200:
            print(f"{Colors.GREEN}[✓] Telegram Broadcast Success!{Colors.END}", flush=True)
        else:
            print(f"{Colors.RED}[- Telegram Send Error]: {res.text}{Colors.END}", flush=True)
    except Exception as e:
        print(f"{Colors.RED}[- Telegram Connection Warning]: {e}{Colors.END}", flush=True)

def fetch_data():
    global last_checked_issue
    
    # 100% Expire မဖြစ်စေရန် လက်ရှိ Dynamic Unix Timestamp ကို အသုံးပြုခြင်း
    current_timestamp = int(time.time())
    
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {GAME_API_TOKEN}" if not GAME_API_TOKEN.startswith("Bearer ") else GAME_API_TOKEN,
        "Ar-Origin": "https://www.cklottery.top",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    payload = {
        "pageSize": 1, # မလိုအပ်ဘဲ Data ရှုပ်မနေအောင် နောက်ဆုံးပွဲစဉ် ၁ ခုပဲ ယူမည်
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

                    # ပွဲစဉ်အသစ် အမှန်တကယ် ထွက်လာမှသာ Message ပို့ရန် စစ်ဆေးခြင်း
                    if issue != last_checked_issue:
                        last_checked_issue = issue
                        
                        # ကျလာတဲ့ အရောင်အလိုက် အလှဆင်မည့် Emoji ခွဲခြားခြင်း
                        emoji = "🟢" if "GREEN" in colour else "🔴" if "RED" in colour else "🟣"
                        if "VIOLET" in colour and ("RED" in colour or "GREEN" in colour):
                            emoji = "🔮"

                        # Telegram သို့ ထွက်မည့် စတိုင်ကျ Premium Markdown ပုံစံ
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
                        
                        # Terminal / Railway Log တွင် လှပစွာ ပြသရန်
                        print(f"\n{Colors.BOLD}{Colors.CYAN}[+] New Result Detected! Issue: {issue}{Colors.END}", flush=True)
                        print(f"{Colors.YELLOW}Number: {num} | Colour: {colour}{Colors.END}", flush=True)
                        
                        # Telegram သို့ ပို့လွှတ်ခြင်း
                        send_telegram_signal(tg_text)
                    else:
                        # ပွဲစဉ်အသစ် မထွက်သေးပါက Log ထဲတွင် အစက်လေးများ ပြပေးနေမည်
                        sys.stdout.write(".")
                        sys.stdout.flush()
            else:
                print(f"\n{Colors.RED}[-] API Exception Alert: {result.get('msg')}{Colors.END}", flush=True)
        elif response.status_code == 401:
            print(f"\n{Colors.RED}[❌ AUTH ERROR] Game Token သက်တမ်းကုန်ဆုံးသွားပါပြီ။ GAME_API_TOKEN ကို အသစ်ပြန်လဲပေးပါ။{Colors.END}", flush=True)
        else:
            print(f"\n{Colors.RED}[-] HTTP Sync Failed: Status {response.status_code}{Colors.END}", flush=True)
            
    except Exception as e:
        print(f"\n{Colors.RED}[- Network Disconnected]: Reconnecting in next loop... ({e}){Colors.END}", flush=True)

if __name__ == "__main__":
    # Screen ကို Clear လုပ်ပြီး လှပစွာ စတင်ခြင်း
    print("\033[H\033[J", end="") 
    print(f"{Colors.BOLD}{Colors.GREEN}[*] 🚀 System Online! Automated Telegram Sync Mode Activated...{Colors.END}", flush=True)
    print("[*] Monitoring 30S API Live Streams...", flush=True)
    
    while True:
        fetch_data()
        time.sleep(4) # API ကို ၄ စက္ကန့်တစ်ခါ အမြန်နှုန်းဖြင့် Live စောင့်ကြည့်ပြီး ပွဲသစ်ထွက်သည်နှင့် ချက်ချင်း ဖမ်းယူမည်
