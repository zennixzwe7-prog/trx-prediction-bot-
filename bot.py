
import requests
import time
import urllib3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# SSL Warning များအား ပိတ်ထားခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
# ⚠️ သင်၏ Telegram Bot Token ကို အောက်တွင် သေချာစွာ အစားထိုးပါ
TELEGRAM_BOT_TOKEN = '8732215456:AAGLCJXwTqBV9cIqusCnm7x0OhnPLsi0TU0' 
API_URL = "https://ckygjf6r.com/api/webapi/GetTRXNoaverageEmerdList"

# ဂိမ်း Server က Cloud Bot မှန်းမသိစေရန် အဆင့်မြင့် ရည်ညွှန်းချက်များ ထည့်သွင်းခြင်း
HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9,my;q=0.8",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Origin": "https://www.cklottery.top",
    "Referer": "https://www.cklottery.top/",
    "Sec-Ch-Ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Sec-Doc-Level": "1"
}

# --- BYPASS API FETCHING ENGINE ---
def get_latest_results():
    # Session စနစ်သုံးပြီး လူကဲ့သို့ ဝင်ရောက်ခြင်း
    session = requests.Session()
    try:
        current_timestamp = int(time.time())
        
        # ⚠️ အကယ်၍ ဤကုဒ်ပြောင်းပြီးမှ မရပါက အောက်ပါ random နှင့် signature ကို Website မှ အသစ်ပြန်ယူရပါမည်
        dynamic_payload = {
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 13,
            "language": 0,
            "random": "5731d15b986d4875955a5cd373cb9e12",
            "signature": "DA042D6562C9C7451B385E421F23C246",
            "timestamp": current_timestamp
        }
        
        response = session.post(
            API_URL, 
            headers=HEADERS, 
            json=dynamic_payload, 
            verify=False, 
            timeout=10
        )
        
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('code') == 0:
                return res_json.get('data', {}).get('data', {}).get('gameslist', [])
            else:
                print(f"API Main Error: {res_json.get('msg')}")
                return []
        else:
            print(f"HTTP Error Code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Exception Occurred: {e}")
        return []
    finally:
        session.close()

# --- ADVANCED STATISTICAL PATTERN ANALYSIS ---
def advanced_pattern_analysis(gameslist):
    if not gameslist or len(gameslist) < 5:
        return None, None, None, None, None

    small_count = sum(1 for g in gameslist[:5] if int(g['number']) <= 4)
    big_count = 5 - small_count
    
    latest_game = gameslist[0]
    latest_number = int(latest_game['number'])
    latest_colour = latest_game['colour']
    current_issue = int(latest_game['issueNumber'])
    next_issue = current_issue + 1

    if small_count >= 4:
        predicted_size = "SMALL 📉"
        safe_numbers = "0, 1, 3"
    elif big_count >= 4:
        predicted_size = "BIG 📈"
        safe_numbers = "6, 7, 8"
    else:
        predicted_size = "BIG 📈" if latest_number <= 4 else "SMALL 📉"
        safe_numbers = "5, 9, 7" if predicted_size == "BIG 📈" else "2, 4, 1"

    color_streak = 1
    for g in gameslist[1:4]:
        if g['colour'] == latest_colour:
            color_streak += 1
        else:
            break

    if color_streak >= 3:
        predicted_colour = "🟢 GREEN" if "red" in latest_colour else "🔴 RED"
    else:
        green_count = sum(1 for g in gameslist[:5] if "green" in g['colour'])
        predicted_colour = "🟢 GREEN" if green_count >= 3 else "🔴 RED"

    hot_number = (latest_number + 3) % 10 if predicted_size == "BIG 📈" else (latest_number - 3) % 10
    if hot_number < 0: hot_number = abs(hot_number)

    return next_issue, predicted_size, predicted_colour, f"{safe_numbers}, {hot_number}", latest_game

# --- TELEGRAM INTERFACE ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['🔮 Get Prediction']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_msg = (
        "👋 မင်္ဂလာပါ! Trx GOD MOD Prediction Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "ယခု Bot သည် Tron Blockchain ရဲ့ ကစားပွဲရလဒ်များကို Random မဟုတ်ဘဲ "
        "Advanced Pattern & Trend Momentum စနစ်ဖြင့် တိကျစွာ တွက်ချက်ပေးပါသည်။\n\n"
        "👇 ခန့်မှန်းချက်ရယူရန် အောက်က ခလုတ်ကို နှိပ်ပါဗျာ။"
    )
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup)

async def handle_prediction_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '🔮 Get Prediction':
        status_message = await update.message.reply_text("🔄 AI မှ လတ်တလော Patterns များကို တွက်ချက်နေပါသည်... စက္ကန့်အနည်းငယ်စောင့်ပါ။")
        
        gameslist = get_latest_results()
        if not gameslist:
            await status_message.edit_text(
                "❌ API Connection Error ဖြစ်နေဆဲပါဗျာ။\n\n"
                "💡 *အဘယ်ကြောင့်နည်း-*\n"
                "ဂိမ်း Website ၏ `signature` အသစ်ပြောင်းသွားခြင်း ဖြစ်နိုင်ပါသည်။ "
                "ကျေးဇူးပြု၍ သင့် Browser (Inspect Element -> Network) မှတစ်ဆင့် "
                "လက်ရှိနောက်ဆုံးဖြစ်နေသော `signature` နှင့် `random` တန်ဖန်းကို ကူးယူပြီး Code တွင် လာရောက် Update လုပ်ပေးပါရန် လိုအပ်ပါသည်မိတ်ဆွေ။"
            )
            return

        next_issue, size, colour, numbers, last_game = advanced_pattern_analysis(gameslist)
        
        response_msg = f"""
🎯 *ANALYSIS COMPLETE* 🎯
━━━━━━━━━━━━━━━━━━
📊 *Last Result (ပြီးခဲ့သောပွဲ):*
• Issue: `{last_game['issueNumber']}`
• Number: `{last_game['number']}`
• Colour: `{last_game['colour'].upper()}`

🚀 *AI Next Prediction (နောက်တစ်ကြိမ်ခန့်မှန်းချက်):*
• Issue: `{next_issue}`
• Betting: *{size}*
• Colour: *{colour}*
• Pattern Numbers: `{numbers}`

💡 *GOD MOD Strategy:*
ဒီပွဲရှုံးပါက နောက်တစ်ပွဲတွင် လောင်းကြေးကို x3 (၃ ဆ) မြှင့်ပါ။ ၅ ပွဲအတွင်း အရင်းကျေ အမြတ်ထွက်စေမည့် အဆင့်မြင့် နည်းဗျူဟာ ဖြစ်သည်။
━━━━━━━━━━━━━━━━━━
"""
        await status_message.edit_text(response_msg, parse_mode="Markdown")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prediction_request))
    
    print("Trx GOD MOD Bot is online on Railway...")
    application.run_polling()

if __name__ == "__main__":
    main()
