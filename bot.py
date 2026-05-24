import requests
import time
import urllib3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# SSL Warning များအားလုံးကို ပိတ်ထားခြင်း (Railway Environment အတွက်)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
# ⚠️ မိမိ၏ Telegram Bot Token ကို ဤနေရာတွင် အစားထိုးပါ
TELEGRAM_BOT_TOKEN = '8732215456:AAGLCJXwTqBV9cIqusCnm7x0OhnPLsi0TU0' 

API_URL = "https://ckygjf6r.com/api/webapi/GetNoaverageEmerdList"

# မိတ်ဆွေပေးပို့ထားသော Headers အသစ်အတိုင်း တိကျစွာ ပြင်ဆင်ခြင်း
HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzc5NTk3MjExIiwibmJmIjoiMTc3OTU5NzIxMSIsImV4cCIOiIjMTc3OTU5OTAxMSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvZXhwaXJhdGlvbiI6IjUvMjQvMjAyNiAxMTozMzozMSBBTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjQ4NzIwMyIsIlVzZXJOYW1lIj6Ijk1OTc3NzU0NTU4OSIsIlVzZXJQaG90byI6IjIwIiwiTmlja05hbWUiOiJNR1RIQU5UICIsIkFtb3VudCI6IjIuMTEiLCJJbnRlZ3JhbCI6IjAiLCJMb2dpbk1hcmsiOiJINSIsIkxvZ2luVGltZSI6IjUvMjQvMjAyNiAxMTowMzozMSBBTSIsIkxvZ2luSVBBZGRyZXNzIjoiMTE2LjIwNi4xOTMuNDAiLCJEYk51bWJlciI6IjAiLCJJc3ZhbGlkYXRvciI6IjAiLCJLZXlDb2RlIjoiNjA0IiwiVG9rZW5UeXBlIjoiQWNjZXNzX1Rva2VuIiwiUGhvbmVUeXBlIjoiMSIsIlVzZXJUeXBlIjoiMCIsIlVzZXJOYW1lMiI6IiIsImlzcyI6Imp3dElzc3VlciIsImF1ZCI6ImxvdHRlcnlUaWNrZXQifQ.DBDcoABNDDdBBPYKY6szyG2kPWVovMHvAOUBFrJpwrY",
    "Ar-Origin": "https://www.cklottery.top",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

# --- NEW API FETCHING ENGINE ---
def get_latest_results():
    session = requests.Session()
    try:
        # မိတ်ဆွေ ပေးပို့ထားသော Request Data (Payload) အသစ်အတိုင်း တိုက်ရိုက်ပုံဖော်ခြင်း
        payload = {
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 30,
            "language": 0,
            "random": "31bb08637448470484669efce0dd10a0",
            "signature": "F73B8B395B8A8E4AE6FD911CE75AAB94",
            "timestamp": 1779600418
        }
        
        response = session.post(API_URL, headers=HEADERS, json=payload, verify=False, timeout=12)
        
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('code') == 0:
                # API Response အသစ်၏ 'data' -> 'list' ထဲမှ ပွဲစဉ်ဒေတာများကို ဆွဲထုတ်ခြင်း
                return res_json.get('data', {}).get('list', [])
        print(f"API Bad Response Log: {response.text}")
        return []
    except Exception as e:
        print(f"Bypass Exception Handled: {e}")
        return []
    finally:
        session.close()

# --- PROFESSIONAL STATISTICAL ANALYSIS ENGINE ---
def advanced_pattern_analysis(gameslist):
    try:
        if not gameslist or len(gameslist) < 5:
            return None, None, None, None, None

        # လတ်တလော ထွက်ထားသော ၅ ပွဲ၏ ဒေတာများကို သုံးသပ်ခြင်း
        small_count = sum(1 for g in gameslist[:5] if int(g['number']) <= 4)
        big_count = 5 - small_count
                
        latest_game = gameslist[0]
        latest_number = int(latest_game['number'])
        current_issue = int(latest_game['issueNumber'])
        next_issue = current_issue + 1

        # Trend Momentum resolution
        if small_count >= 4:
            predicted_size = "SMALL 📉"
            safe_numbers = "0, 1, 2"
        elif big_count >= 4:
            predicted_size = "BIG 📈"
            safe_numbers = "5, 7, 9"
        else:
            predicted_size = "BIG 📈" if latest_number <= 4 else "SMALL 📉"
            safe_numbers = "6, 8, 9" if predicted_size == "BIG 📈" else "1, 3, 4"

        # Multi-color algorithm
        green_count = sum(1 for g in gameslist[:5] if "green" in g['colour'])
        predicted_colour = "🟢 GREEN" if green_count >= 3 else "🔴 RED"

        hot_number = (latest_number + 4) % 10 if predicted_size == "BIG 📈" else (latest_number - 2) % 10
        if hot_number < 0: hot_number = abs(hot_number)

        return next_issue, predicted_size, predicted_colour, f"{safe_numbers}, {hot_number}", latest_game
    except Exception as ae:
        print(f"Analysis Algorithm Error: {ae}")
        return None, None, None, None, None

# --- TELEGRAM USER INTERFACE ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['🔮 Get Prediction']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    welcome_msg = "🔥 *TRX GOD MOD V3 (REBUILT COMPLETE)* 🔥\n\nAPI အသစ်ဖြင့် အစအဆုံး ပြန်လည်မောင်းနှင်ထားပါသည်။\n\n👇 ခန့်မှန်းချက်ရယူရန် အောက်က ခလုတ်ကို နှိပ်ပါဗျာ။"
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_prediction_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '🔮 Get Prediction':
        status_message = await update.message.reply_text("🔄 AI မှ API ဒေတာသစ်များကို ရယူပြီး Patterns တွက်ချက်နေပါသည်...")
        
        try:
            gameslist = get_latest_results()
            if not gameslist:
                await status_message.edit_text(
                    "❌ *ဒေတာဆွဲယူ၍ မရနိုင်သေးပါ မိတ်ဆွေ။*\n\n"
                    "💡 *အကြောင်းအရင်း-*\n"
                    "မိတ်ဆွေပေးထားသော Token သို့မဟုတ် Signature သက်တမ်းကုန်သွားခြင်း ဖြစ်နိုင်ပါသည်။ "
                    "Browser (Inspect) ထဲမှ `signature` ၊ `random` နှင့် `Authorization` အသစ်များကို ကုဒ်ထဲတွင် အစားထိုးပေးပါရန် လိုအပ်ပါသည်။"
                )
                return

            next_issue, size, colour, numbers, last_game = advanced_pattern_analysis(gameslist)
            
            if not next_issue:
                await status_message.edit_text("⚠️ Data Structure လွဲမှားနေပါသည်။ ခဏစောင့်ပြီး ပြန်နှိပ်ကြည့်ပါ။")
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
            print(f"Crash Prevented in Handler: {handler_error}")
            try:
                await status_message.edit_text("⚠️ စနစ်အတွင်း ယာယီ Error ဖြစ်ပွားသွားပါသည်။ ခဏနေမှ ပြန်ကြိုးစားပါ။")
            except:
                pass

def main():
    while True: # Railway ပေါ်တွင် ကုဒ်လုံးဝမရပ်သွားစေရန် Infinite Crash-Safe Loop တပ်ဆင်ထားခြင်း
        try:
            print("Launching Trx Rebuilt V3 Engine...")
            application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
            application.add_handler(CommandHandler("start", start))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prediction_request))
            
            application.run_polling(drop_pending_updates=True)
        except Exception as loop_error:
            print(f"Critical Main Loop Error caught: {loop_error}. Restarting in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()
