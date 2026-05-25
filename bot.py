import os
import asyncio
import logging
import random
import requests

from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Bot
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# =========================================
# CONFIG
# =========================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@lotteryprde"

API_URL = "https://ckygjf6r.com/api/webapi/GetNoaverageEmerdList"

AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzc5NjczNTAxIiwibmJmIjoiMTc3OTY3MzUwMSIsImV4cCI6IjE3Nzk2NzUzMDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI1LzI1LzIwMjYgODo0NTowMSBBTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjQ4NzIwMyIsIlVzZXJOYW1lIjoiOTU5Nzc3NTQ1NTg5IiwiVXNlclBob3RvIjoiMjAiLCJOaWNrTmFtZSI6Ik1HVEhBTlQgIiwiQW1vdW50IjoiMi42MSIsIkludGVncmFsIjoiMCIsIkxvZ2luTWFyayI6Ikg1IiwiTG9naW5UaW1lIjoiNS8yNS8yMDI2IDg6MTU6MDEgQU0iLCJMb2dpbklQQWRkcmVzcyI6IjExNi4yMDYuMTkzLjQwIiwiRGJOdW1iZXIiOiIwIiwiSXN2YWxpZGF0b3IiOiIwIiwiS2V5Q29kZSI6IjYwNSIsIlRva2VuVHlwZSI6IkFjY2Vzc19Ub2tlbiIsIlBob25lVHlwZSI6IjEiLCJVc2VyVHlwZSI6IjAiLCJVc2VyTmFtZTIiOiIiLCJpc3MiOiJqd3RJc3N1ZXIiLCJhdWQiOiJsb3R0ZXJ5VGlja2V0In0.x3qj70HmHJKnSsYTI08LqurJ-KB4W7e0syYMwPWfbvE"

# =========================================
# LOGGING
# =========================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================================
# TELEGRAM BOT
# =========================================

bot = Bot(token=BOT_TOKEN)

# =========================================
# API FETCH
# =========================================

def fetch_data():

    timestamp = int(datetime.now().timestamp())

    payload = {
        "pageSize": 10,
        "pageNo": 1,
        "typeId": 30,
        "language": 0,
        "random": "be8d0ae92c154507a735d86a2d792cd3",
        "signature": "DBDC04A4BEB3AAAB575F34FD0B4C6872",
        "timestamp": timestamp
    }

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Ar-Origin": "https://www.cklottery.top",
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; Mobile) "
            "AppleWebKit/537.36 Chrome/124.0.0.0 "
            "Mobile Safari/537.36"
        )
    }

    response = requests.post(
        API_URL,
        json=payload,
        headers=headers,
        timeout=15
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code != 200:
        raise Exception(f"HTTP ERROR {response.status_code}")

    if not response.text.strip():
        raise Exception("EMPTY RESPONSE")

    return response.json()

# =========================================
# PREDICTION LOGIC
# =========================================

def analyze_prediction(numbers):

    latest = numbers[:5]

    avg = sum(latest) / len(latest)

    red = len([x for x in latest if x in [0,2,4,6,8]])
    green = len([x for x in latest if x in [1,3,5,7,9]])

    # BIG SMALL

    if avg >= 5:
        big_small = "BIG"
    else:
        big_small = "SMALL"

    # COLOR

    if red > green:
        color = "GREEN"
    else:
        color = "RED"

    # NUMBER

    prediction_number = random.randint(0, 9)

    return big_small, color, prediction_number

# =========================================
# GET PREDICTION
# =========================================

def get_prediction():

    try:

        data = fetch_data()

        games = data["data"]["list"]

        numbers = []

        for game in games:
            numbers.append(int(game["number"]))

        big_small, color, number = analyze_prediction(numbers)

        current_time = datetime.now(
            ZoneInfo("Asia/Yangon")
        ).strftime("%Y-%m-%d %I:%M:%S %p")

        return {
            "time": current_time,
            "period": games[0]["issueNumber"],
            "prediction": big_small,
            "color": color,
            "number": number,
            "status": "SUCCESS"
        }

    except Exception as e:

        return {
            "time": "-",
            "period": "-",
            "prediction": "-",
            "color": "-",
            "number": "-",
            "status": str(e)
        }

# =========================================
# START COMMAND
# =========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [

        [
            InlineKeyboardButton(
                "🎯 Predict",
                callback_data="predict"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 TRX GOD MOD ONLINE",
        reply_markup=reply_markup
    )

# =========================================
# BUTTON HANDLER
# =========================================

async def button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    result = get_prediction()

    text = f"""
🔥 LIVE PREDICTION

⏰ MM Time: {result['time']}

📌 Period: {result['period']}

📈 Big/Small: {result['prediction']}
🎨 Color: {result['color']}
🔢 Number: {result['number']}

✅ Status: {result['status']}
"""

    await query.edit_message_text(text)

# =========================================
# /predict
# =========================================

async def predict(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    result = get_prediction()

    text = f"""
🔥 LIVE PREDICTION

⏰ MM Time: {result['time']}

📌 Period: {result['period']}

📈 Big/Small: {result['prediction']}
🎨 Color: {result['color']}
🔢 Number: {result['number']}

✅ Status: {result['status']}
"""

    await update.message.reply_text(text)

# =========================================
# AUTO SIGNAL
# =========================================

async def auto_prediction():

    while True:

        try:

            result = get_prediction()

            text = f"""
🔥 AUTO SIGNAL

⏰ MM Time: {result['time']}

📌 Period: {result['period']}

📈 Prediction: {result['prediction']}
🎨 Color: {result['color']}
🔢 Number: {result['number']}

✅ {result['status']}
"""

            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=text
            )

            print("SIGNAL SENT")

        except Exception as e:

            print("AUTO ERROR:", e)

        # EVERY 30 SECONDS
        await asyncio.sleep(30)

# =========================================
# MAIN
# =========================================

async def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("predict", predict)
    )

    app.add_handler(
        CallbackQueryHandler(button)
    )

    asyncio.create_task(
        auto_prediction()
    )

    print("BOT RUNNING...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)

# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    asyncio.run(main())
