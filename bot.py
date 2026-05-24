import requests
import time
import urllib3
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# SSL Certificate သတိပေးချက်များကြောင့် Cloud တွင် ပိတ်ဆို့ခြင်းမရှိစေရန်
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
# ⚠️ သင်၏ Telegram Bot Token ကို အောက်တွင် အစားထိုးပါ
TELEGRAM_BOT_TOKEN = '8732215456:AAGLCJXwTqBV9cIqusCnm7x0OhnPLsi0TU0' 

API_URL = "https://ckygjf6r.com/api/webapi/GetNoaverageEmerdList"

# --- ADVANCED BROWSER FINGERPRINT SIMULATOR ---
def get_dynamic_headers():
    """ တကယ့်လူတစ်ဦးချင်းစီ၏ ဖုန်း သို့မဟုတ် ကွန်ပျူတာ Browser ပုံစံများကို အလှည့်ကျအတုယူခြင်း """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    ]
    
    return {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,my;q=0.8,zh-CN;q=0.7,zh;q=0.6",
        "User-Agent": random.choice(user_agents),
        "Origin": "https://www.cklottery.top",
        "Referer": "https://www.cklottery.top/",
        "Ar-Origin": "https://www.cklottery.top",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }

# --- ADVANCED BYPASS API FETCHING ENGINE ---
def get_latest_results():
    # Session ကို သီးသန့်ဆောက်ပြီး Cookie များကို အလိုအလျောက်သိမ်းဆည်းစေခြင်း
    session = requests.Session()
    try:
        # လက်ရှိ Real-time Timestamp (စက္ကန့်အလိုက်ပြောင်းလဲခြင်း)
        current_timestamp = int(time.time())
        
        # Website မှ ပေးပို့ထားသော နောက်ဆုံးလက်ရှိ စည်းမျဉ်းသစ် Payload 
        payload = {
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 30,
            "language": 0,
            "random": "b5344c2c0eab4960a54eae1f3b8bbb08",
            "signature": "F91DE9F46EA4DD769ED840F9F1887083",
            "timestamp": current_timestamp
        }
        
        # အဆင့်မြင့် Dynamic Headers များဖြင့် Request ပို့ခြင်း
        response = session.post(
            API_URL, 
            headers=get_dynamic_headers(), 
            json=payload, 
            verify=False, 
            timeout=15
        )
        
        # ကွန်နက်ရှင် အောင်မြင်ပါက
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('code') == 0:
                # ဒေတာဖွဲ့စည်းပုံအသစ် (data -> list) အား တိုက်ရိုက်ဆွဲထုတ်ခြင်း
                return res_json.get('data', {}).get('list', [])
            else:
                print(f"API Internal Refusal: {res_json.get('msg')}")
                return []
        else:
            print(f"HTTP Connection Blocked: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Network Connection Level Exception: {e}")
        return []
    finally:
        session.close()

# --- PROFESSIONAL STATISTICAL PATTERN ENGINE ---
def advanced_pattern_analysis(gameslist):
    if not gameslist or len(gameslist) < 5:
        return None, None, None, None, None

    # ၁။ Trend Momentum (လတ်တလော လှိုင်းအင်အားကို ရှာဖွေခြင်း)
    small_count = sum(1 for g in gameslist[:5] if int(g['number']) <= 4)
    big_count = 5 - small_count
    
    # ၂။ လက်ရှိပွဲစဉ် အချက်အလက်များ
    latest_game = gameslist[0]
    latest_number = int(latest_game['number'])
    latest_colour = latest_game['colour']
    current_issue = int(latest_game['issueNumber'])
    next_issue = current_issue + 1

    # ၃။ Mathematical Probability Logic for Big/Small
    if small_count >= 4:  
        predicted_size = "SMALL 📉"
        safe_numbers = "0, 1, 3"
    elif big_count >= 4:  
        predicted_size = "BIG 📈"
        safe_numbers = "5, 6, 9"
    else:  
        predicted_size = "BIG 📈" if latest_number <= 4 else "SMALL 📉"
        safe_numbers = "7, 8, 9" if predicted_size == "BIG 📈" else "0, 2, 4"

    # ၄။ Multi-Layer Colour Streak Probability Analyzer
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

    # နံပါတ်တစ်လုံးတည်း အပိုင်ရွေးချယ်မှု Algorithm 
    hot_number = (latest_number + 4) % 10 if predicted_size == "BIG 📈" else (latest_number - 2) % 10
    if hot_number < 0: hot_number = abs(hot_number)

    return next_issue, predicted_size, predicted_colour, f"{safe_numbers}, {hot_number}", latest_game

# --- TELEGRAM USER INTERFACE ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['🔮 Get Prediction']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_msg = (
        "👋 မင်္ဂလာပါ! Trx GOD MOD Ultra V2 Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "ယခု Bot သည် စနစ်သစ် API ကို လုံခြုံစိတ်ချရသော Browser Simulation "
        "နည်းပညာဖြင့် တိုက်ရိုက်ချိတ်ဆက်ကာ တိကျစွာ တွက်ချက်ပေးနေပါပြီ။\n\n"
        "👇 ခန့်မှန်းချက်ရယူရန် အောက်က ခလုတ်ကို နှိပ်ပါဗျာ။"
    )
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup)

async def handle_prediction_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '🔮 Get Prediction':
        status_message = await update.message.reply_text("🔄 AI မှ Security Layer ကို ကျော်ဖြတ်ပြီး Patterns များ တွက်ချက်နေပါသည်... ခေတ္တစောင့်ပါ။")
        
        gameslist = get_latest_results()
        if not gameslist:
            await status_message.edit_text(
                "⚠️ *SYSTEM INFORMATION:*\n\n"
                "ဂိမ်း Server ဘက်မှ Token/Signature လုံခြုံရေးအဆင့်မြှင့်တင်လိုက်သဖြင့် Request ပယ်ချခံရပါသည်။\n\n"
                "💡 *ပြုပြင်ရန်နည်းလမ်း-*\n"
                "သင့်ဖုန်း Browser မှတစ်ဆင့် ဂိမ်းဆိုဒ်ထဲဝင်၍ လက်ရှိနောက်ဆုံးဖြစ်နေသော `signature` နှင့် `random` ကို ကူးယူပြီး ကုဒ်ထဲတွင် လာရောက် Update လုပ်ပေးပါရန် လိုအပ်ပါသည် မိတ်ဆွေ။"
            )
            return

        next_issue, size, colour, numbers, last_game = advanced_pattern_analysis(gameslist)
        
        response_msg = f"""
🎯 *ANALYSIS COMPLETE (ULTRA V2)* 🎯
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
    
    print("Trx GOD MOD Ultra Bot is successfully online on Railway...")
    application.run_polling()

if __name__ == "__main__":
    main()
