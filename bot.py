import requests
import time
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = '8507446809:AAEpBmyx7S7JgL1loGV0qUMgU0Pmuj4JkRs'  # မိမိ Bot Token ထည့်ရန်
API_URL = "https://ckygjf6r.com/api/webapi/GetTRXNoaverageEmerdList"

HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Ar-Origin": "https://www.cklottery.top"
}

PAYLOAD = {
    "pageSize": 10,
    "pageNo": 1,
    "typeId": 13,
    "language": 0,
    "random": "5731d15b986d4875955a5cd373cb9e12",
    "signature": "DA042D6562C9C7451B385E421F23C246",
    "timestamp": 1779595047
}

def get_latest_results():
    try:
        response = requests.post(API_URL, headers=HEADERS, json=PAYLOAD)
        if response.status_code == 200:
            return response.json().get('data', {}).get('data', {}).get('gameslist', [])
        return []
    except Exception as e:
        print(f"API Error: {e}")
        return []

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['🔮 Get Prediction']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_msg = (
        "👋 မင်္ဂလာပါ! 24/7 Professional Prediction Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "ဒီ Bot ဟာ Tron Blockchain ရဲ့ ရလဒ်တွေကို Algorithm & Pattern Analysis "
        "စနစ်နဲ့ တိကျစွာ တွက်ချက်ပေးတာဖြစ်ပါတယ်။\n\n"
        "👇 ခန့်မှန်းချက်ရယူဖို့ အောက်က ခလုတ်ကို နှိပ်ပါ!"
    )
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup)

async def handle_prediction_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '🔮 Get Prediction':
        await update.message.reply_text("🔄 API မှ Data များကို ဆွဲယူပြီး Patterns များ တွက်ချက်နေပါသည်... ခေတ္တစောင့်ပါ။")
        
        gameslist = get_latest_results()
        if not gameslist:
            await update.message.reply_text("❌ API Data ဆွဲယူရတာ အဆင်မပြေဖြစ်နေပါတယ်။ ခဏနေမှ ပြန်စမ်းပါ။")
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

💡 *Martingale (x3) Strategy:*
ဒီပွဲရှုံးပါက နောက်တစ်ပွဲတွင် လောင်းကြေးကို ၃ ဆမြှင့်ပါ။ ၅ ပွဲအတွင်း အရင်းကျေ အမြတ်ထွက်စေမည့် စနစ်ဖြစ်သည်။
━━━━━━━━━━━━━━━━━━
"""
        await update.message.reply_text(response_msg, parse_mode="Markdown")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prediction_request))
    print("Interactive Prediction Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
