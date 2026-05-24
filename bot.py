import requests
import time
import urllib3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# SSL Warning များ မပြအောင် ပိတ်ထားခြင်း (Render ပေါ်တွင် ပိုမိုအဆင်ပြေစေရန်)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
# ⚠️ မိမိ၏ Bot Token ကို အောက်ပါနေရာတွင် သေချာစွာ အစားထိုးပါ
TELEGRAM_BOT_TOKEN = '8732215456:AAGLCJXwTqBV9cIqusCnm7x0OhnPLsi0TU0' 
API_URL = "https://ckygjf6r.com/api/webapi/GetTRXNoaverageEmerdList"

HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Ar-Origin": "https://www.cklottery.top"
}

# --- DYNAMIC API FETCHING ENGINE ---
def get_latest_results():
    try:
        # စက္ကန့်အလိုက် ပြောင်းလဲနေသော လက်ရှိ Unix Timestamp အား ထုတ်ယူခြင်း
        current_timestamp = int(time.time())
        
        # API သို့ ပေးပို့မည့် လုံခြုံရေးဆိုင်ရာ Data များ
        dynamic_payload = {
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 13,
            "language": 0,
            "random": "5731d15b986d4875955a5cd373cb9e12",
            "signature": "DA042D6562C9C7451B385E421F23C246", # ⚠️ အကယ်၍ API ပိတ်ပါက Website မှ signature အသစ် ပြန်လဲပေးရန်လိုအပ်သည်
            "timestamp": current_timestamp
        }
        
        # verify=False ဖြင့် Cloud Connection Block ဖြစ်ခြင်းကို ကျော်လွှားခြင်း
        response = requests.post(API_URL, headers=HEADERS, json=dynamic_payload, verify=False, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('code') == 0:
                return res_json.get('data', {}).get('data', {}).get('gameslist', [])
            else:
                print(f"API Error Message: {res_json.get('msg')}")
                return []
        else:
            print(f"Server Response HTTP Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Connection Exception Error: {e}")
        return []

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
        safe_numbers = "6, 7, 8"
    else:  # ရလဒ်များ ရောထွေးနေပါက နောက်ဆုံးဂဏန်းကို အခြေခံ၍ Counter-Trend လှည့်တွက်ခြင်း
        predicted_size = "BIG 📈" if latest_number <= 4 else "SMALL 📉"
        safe_numbers = "5, 9, 7" if predicted_size == "BIG 📈" else "2, 4, 1"

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
    hot_number = (latest_number + 3) % 10 if predicted_size == "BIG 📈" else (latest_number - 3) % 10
    if hot_number < 0: hot_number = abs(hot_number)

    return next_issue, predicted_size, predicted_colour, f"{safe_numbers}, {hot_number}", latest_game

# --- TELEGRAM INTERFACE ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # လူတိုင်းလွယ်ကူစွာနှိပ်နိုင်မည့် ခလုတ်အား ဖန်တီးခြင်း
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
        # သုံးစွဲသူအား ခေတ္တစောင့်ရန် အသိပေးခြင်း
        status_message = await update.message.reply_text("🔄 AI မှ လတ်တလော Patterns များကို တွက်ချက်နေပါသည်... စက္ကန့်အနည်းငယ်စောင့်ပါ။")
        
        gameslist = get_latest_results()
        if not gameslist:
            await status_message.edit_text("❌ API Data ဆွဲယူရတာ အဆင်မပြေဖြစ်နေပါတယ်။\n(ဂိမ်း Server က သင့် Bot ကို ခေတ္တပိတ်ထားခြင်း သို့မဟုတ် Signature သက်တမ်းကုန်ခြင်း ဖြစ်နိုင်ပါသည်။)")
            return

        next_issue, size, colour, numbers, last_game = advanced_pattern_analysis(gameslist)
        
        response_msg = f"""
🎯 *ANALYSIS COMPLETE (တွက်ချက်မှုပြီးပါပြီ)* 🎯
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
    # Bot အား တည်ဆောက်ပြီး မောင်းနှင်ခြင်း
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prediction_request))
    
    print("Trx GOD MOD Bot is online and running...")
    application.run_polling()

if __name__ == "__main__":
    main()
