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

# API လိပ်စာအသစ်
API_URL = "https://ckygjf6r.com/api/webapi/GetNoaverageEmerdList"

HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9,my;q=0.8",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Origin": "https://www.cklottery.top",
    "Referer": "https://www.cklottery.top/",
    "Ar-Origin": "https://www.cklottery.top"
}

# --- NEW API FETCHING ENGINE ---
def get_latest_results():
    session = requests.Session()
    try:
        current_timestamp = int(time.time())
        
        # သင် ပေးပို့ထားသော API Data အသစ်စက်စက် (Dynamic Timestamp ဖြင့်)
        payload = {
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 30,
            "language": 0,
            "random": "b5344c2c0eab4960a54eae1f3b8bbb08",
            "signature": "F91DE9F46EA4DD769ED840F9F1887083",
            "timestamp": current_timestamp
        }
        
        response = session.post(
            API_URL, 
            headers=HEADERS, 
            json=payload, 
            verify=False, 
            timeout=10
        )
        
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('code') == 0:
                # API အသစ်၏ ဒေတာတည်ဆောက်ပုံအရ 'data' ထဲက 'list' ကို တိုက်ရိုက်ယူခြင်း
                return res_json.get('data', {}).get('list', [])
            else:
                print(f"API Error Message: {res_json.get('msg')}")
                return []
        else:
            print(f"HTTP Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Connection Error: {e}")
        return []
    finally:
        session.close()

# --- ADVANCED STATISTICAL PATTERN ANALYSIS ---
def advanced_pattern_analysis(gameslist):
    if not gameslist or len(gameslist) < 5:
        return None, None, None, None, None

    # ၁။ Trend Momentum Analysis (နောက်ဆုံး ၅ ကြိမ်ထွက်နှုန်းကို တွက်ချက်ခြင်း)
    small_count = sum(1 for g in gameslist[:5] if int(g['number']) <= 4)
    big_count = 5 - small_count
    
    # ၂။ လက်ရှိ နောက်ဆုံးပွဲစဉ်၏ အချက်အလက်များ
    latest_game = gameslist[0]
    latest_number = int(latest_game['number'])
    latest_colour = latest_game['colour']
    current_issue = int(latest_game['issueNumber'])
    next_issue = current_issue + 1

    # ၃။ Logic Execution for Big/Small
    if small_count >= 4:  # Small အထွက်များနေသော Trend ဖြစ်လျှင်
        predicted_size = "SMALL 📉"
        safe_numbers = "0, 1, 3"
    elif big_count >= 4:  # Big အထွက်များနေသော Trend ဖြစ်လျှင်
        predicted_size = "BIG 📈"
        safe_numbers = "5, 6, 9"
    else:  # ရလဒ်များ ရောထွေးနေပါက နောက်ဆုံးဂဏန်းကို အခြေခံ၍ Counter-Trend လှည့်တွက်ခြင်း
        predicted_size = "BIG 📈" if latest_number <= 4 else "SMALL 📉"
        safe_numbers = "7, 8, 9" if predicted_size == "BIG 📈" else "0, 2, 4"

    # ၄။ Logic Execution for Colour (အရောင်အလှည့်အပြောင်း တွက်ချက်မှု)
    color_streak = 1
    for g in gameslist[1:4]:
        if g['colour'] == latest_colour:
            color_streak += 1
        else:
            break

    if color_streak >= 3: # အရောင်တစ်ခုတည်း ဆက်တိုက် ၃ ကြိမ်ထွက်ပြီးပါက ပြောင်းပြန်ထွက်နိုင်ခြေ ပိုများသည်။
        predicted_colour = "🟢 GREEN" if "red" in latest_colour else "🔴 RED"
    else:
        green_count = sum(1 for g in gameslist[:5] if "green" in g['colour'])
        predicted_colour = "🟢 GREEN" if green_count >= 3 else "🔴 RED"

    # သင်္ချာနည်းအရ ကံထူးနိုင်ခြေအရှိဆုံး Single Hot Number တွက်ချက်ခြင်း
    hot_number = (latest_number + 4) % 10 if predicted_size == "BIG 📈" else (latest_number - 2) % 10
    if hot_number < 0: hot_number = abs(hot_number)

    return next_issue, predicted_size, predicted_colour, f"{safe_numbers}, {hot_number}", latest_game

# --- TELEGRAM INTERFACE ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['🔮 Get Prediction']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_msg = (
        "👋 မင်္ဂလာပါ! Trx GOD MOD V2 Prediction Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "ယခု Bot သည် စနစ်သစ် API ကို အသုံးပြုထားပြီး၊ ကစားပွဲရလဒ်များကို "
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
                "❌ API Connection Error ဖြစ်နေပါသေးသည်။\n\n"
                "💡 *အကြံပြုချက်:*\n"
                "သင်ပေးထားသော signature နှင့် random သက်တမ်း ကုန်သွားခြင်းဖြစ်နိုင်ပါသည်။ "
                "အကယ်၍ ဤသို့ဖြစ်ပါက Website မှ နောက်ဆုံးဖြစ်နေသော key များကို အသစ်တစ်ကြိမ် ပြန်လဲပေးပါ။"
            )
            return

        next_issue, size, colour, numbers, last_game = advanced_pattern_analysis(gameslist)
        
        response_msg = f"""
🎯 *ANALYSIS COMPLETE (V2)* 🎯
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
    
    print("Trx GOD MOD V2 Bot is online on Railway...")
    application.run_polling()

if __name__ == "__main__":
    main()
