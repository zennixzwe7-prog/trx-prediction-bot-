import requests
import time
import urllib3
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# SSL Warning များအားလုံးကို ပိတ်ထားခြင်း (Railway Environment အတွက်)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
# ⚠️ ၁။ မိမိ၏ Telegram Bot Token ကို ဤနေရာတွင် အစားထိုးပါ
TELEGRAM_BOT_TOKEN = '8732215456:AAGLCJXwTqBV9cIqusCnm7x0OhnPLsi0TU0' 

# ⚠️ ၂။ မိတ်ဆွေပေးထားသော Token ထဲမှ Error တက်စေမည့် စာသားအမှားများကို စနစ်တကျ သန့်စင်ပြီးသားဖြစ်ပါသည်
RAW_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzc5NTk3MjExIiwibmJmIjoiMTc3OTU5"
    "NzIxMSIsImV4cCI6IjE3Nzk1OTkwMTEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIw"
    "MDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI1LzI0LzIwMjYgMTE6MzM6MzEgQU0iLCJo"
    "dHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUi"
    "OiJBY2Nlc3NfVG9rZW4iLCJVc2VySWQiOiI0ODcyMDMiLCJVc2VyTmFtZSI6Ijk1OTc3NzU0NTU4OSIs"
    "IlVzZXJQaG90byI6IjIwIiwiTmlja05hbWUiOiJNR1RIQU5UICIsIkFtb3VudCI6IjIuMTEiLCJJbnRl"
    "Z3JhbCI6IjAiLCJMb2dpbk1hcmsiOiJINSIsIkxvZ2luVGltZSI6IjUvMjQvMjAyNiAxMTowMzozMSBB"
    "TSIsIkxvZ2luSVBBZGRyZXNzIjoiMTE2LjIwNi4xOTMuNDAiLCJEYk51bWJlciI6IjAiLCJJc3ZhbGlk"
    "YXRvciI6IjAiLCJLZXlDb2RlIjoiNjA0IiwiVG9rZW5UeXBlIjoiQWNjZXNzX1Rva2VuIiwiUGhvbmVU"
    "eXBlIjoiMSIsIlVzZXJUeXBlIjoiMCIsIlVzZXJOYW1lMiI6IiIsImlzcyI6Imp3dElzc3VlciIsImF1"
    "ZCI6ImxvdHRlcnlUaWNrZXQifQ.DBDcoABNDDdBBPYKY6szyG2kPWVovMHvAOUBFrJpwrY"
AUTH_TOKEN = f"Bearer {RAW_TOKEN.strip()}"
API_URL = "https://ckygjf6r.com/api/webapi/GetNoaverageEmerdList"

HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Authorization": AUTH_TOKEN,
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Origin": "https://www.cklottery.top",
    "Referer": "https://www.cklottery.top/",
    "Ar-Origin": "https://www.cklottery.top"
}

# --- CRASH-PROOF API ENGINE ---
def get_latest_results():
    session = requests.Session()
    try:
        current_timestamp = int(time.time())
        payload = {
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 30,
            "language": 0,
            "random": "b5344c2c0eab4960a54eae1f3b8bbb08",
            "signature": "F91DE9F46EA4DD769ED840F9F1887083",
            "timestamp": current_timestamp
        }
        
        response = session.post(API_URL, headers=HEADERS, json=payload, verify=False, timeout=10)
        
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('code') == 0:
                return res_json.get('data', {}).get('list', [])
        return []
    except Exception as e:
        print(f"Log Error (Caught & Handled): {e}")
        return []
    finally:
        session.close()

# --- PATTERN ANALYSIS ENGINE ---
def advanced_pattern_analysis(gameslist):
    try:
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
            safe_numbers = "0, 1, 2"
        elif big_count >= 4:
            predicted_size = "BIG 📈"
            safe_numbers = "5, 7, 9"
        else:
            predicted_size = "BIG 📈" if latest_number <= 4 else "SMALL 📉"
            safe_numbers = "6, 8, 9" if predicted_size == "BIG 📈" else "1, 3, 4"

        green_count = sum(1 for g in gameslist[:5] if "green" in g['colour'])
        predicted_colour = "🟢 GREEN" if green_count >= 3 else "🔴 RED"

        hot_number = (latest_number + 4) % 10 if predicted_size == "BIG 📈" else (latest_number - 2) % 10
        if hot_number < 0: hot_number = abs(hot_number)

        return next_issue, predicted_size, predicted_colour, f"{safe_numbers}, {hot_number}", latest_game
    except Exception as analysis_error:
        print(f"Analysis Pattern Error: {analysis_error}")
        return None, None, None, None, None

# --- TELEGRAM CONTROLLER ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = [['🔮 Get Prediction']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        welcome_msg = "🔥 *TRX GOD MOD V3 Activated* 🔥\n\n👇 ခန့်မှန်းချက်ရယူရန် အောက်က ခလုတ်ကို နှိပ်ပါဗျာ။"
        await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode="Markdown")
    except Exception as ce:
        print(f"Start Command Error: {ce}")

async def handle_prediction_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '🔮 Get Prediction':
        status_message = await update.message.reply_text("🔄 AI မှ လတ်တလော ပွဲစဉ် Pattern များကို တွက်ချက်နေပါသည်...")
        
        try:
            gameslist = get_latest_results()
            if not gameslist:
                await status_message.edit_text(
                    "❌ *ဒေတာဆွဲယူ၍ မရနိုင်သေးပါ မိတ်ဆွေ။*\n\n"
                    "💡 *ဖြစ်နိုင်ခြေအချက်များ-*\n"
                    "၁။ ကုဒ်ထဲရှိ `AUTH_TOKEN` (Bearer) သက်တမ်းကုန်သွားခြင်း။\n"
                    "၂။ Website ဘက်မှ signature အသစ် ပြောင်းလဲပစ်လိုက်ခြင်း။\n\n"
                    "သင့်ဖုန်း Browser မှတစ်ဆင့် 'GetNoaverageEmerdList' ရဲ့ `Authorization` သို့မဟုတ် `signature` အသစ်ကို ကူးယူပြီး လဲလှယ်ပေးပါ။"
                )
                return

            next_issue, size, colour, numbers, last_game = advanced_pattern_analysis(gameslist)
            
            if not next_issue:
                await status_message.edit_text("⚠️ Data ပုံစံလွဲမှားနေသဖြင့် ခန့်မှန်း၍မရနိုင်သေးပါ။ ခေတ္တစောင့်ပြီး ပြန်နှိပ်ပါ။")
                return

            response_msg = f"""
🎯 *TRX PREDICTION COMPLETE* 🎯
━━━━━━━━━━━━━━━━━━
📊 *Last Result (ပြီးခဲ့သောပွဲ):*
• Issue: `{last_game['issueNumber']}`
• Number: `{last_game['number']}`
• Colour: `{last_game['colour'].upper()}`

🚀 *AI Ultra Prediction (နောက်တစ်ကြိမ်ခန့်မှန်းချက်):*
• Issue: `{next_issue}`
• Betting: *{size}*
• Colour: *{colour}*
• Pattern Numbers: `{numbers}`

💡 *Professional Strategy:*
ဒီပွဲရှုံးပါက နောက်တစ်ပွဲတွင် လောင်းကြေးကို x3 (၃ ဆ) မြှင့်ပါ။ စိတ်အေးအေးထားပြီး စနစ်တကျဆော့ကစားပါ။
━━━━━━━━━━━━━━━━━━
"""
            await status_message.edit_text(response_msg, parse_mode="Markdown")
            
        except Exception as handler_error:
            print(f"Request Handler Crash Prevented: {handler_error}")
            try:
                await status_message.edit_text("⚠️ ယာယီ Error ဖြစ်ပွားသွားပါသည်။ ကျေးဇူးပြု၍ ခဏနေမှ ပြန်ကြိုးစားပါ။")
            except:
                pass

def main():
    while True: # Railway ပေါ်တွင် ကုဒ်တစ်ခုလုံး မည်သည့်အကြောင်းကြောင့်မျှ မရပ်သွားစေရန် Infinite Loop ထည့်သွင်းထားခြင်း
        try:
            print("Starting Trx GOD MOD Stable Engine...")
            application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
            application.add_handler(CommandHandler("start", start))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prediction_request))
            
            application.run_polling(drop_pending_updates=True)
        except Exception as main_loop_error:
            print(f"Critical Loop Restarting in 5 seconds... Error: {main_loop_error}")
            time.sleep(5)

if __name__ == "__main__":
    main()
