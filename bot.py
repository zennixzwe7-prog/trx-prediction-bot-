import os
import sqlite3
import asyncio
import logging
import requests

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

# =========================
# CONFIG
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

API_URL = "https://ckygjf6r.com/api/webapi/GetNoaverageEmerdList"

CHANNEL_ID = "@lotteryprde"

# =========================
# LOGGING
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# DATABASE
# =========================

conn = sqlite3.connect(
    "prediction.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    result TEXT
)
""")

conn.commit()

# =========================
# TELEGRAM BOT
# =========================

bot = Bot(token=BOT_TOKEN)

# =========================
# FETCH API DATA
# =========================

def fetch_data():

    payload = {
        "pageSize": 20,
        "pageNo": 1,
        "typeId": 30,
        "language": 0,
        "random": "7d6a0880296a4b8d80c573127f0f7f4d",
        "signature": "CE809807A0F316E1FDC6909DDB7B1F0B"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(
        API_URL,
        json=payload,
        headers=headers,
        timeout=10
    )

    return response.json()

# =========================
# SMART PREDICTION
# =========================

def smart_prediction(numbers):

    avg = sum(numbers) / len(numbers)

    odd = len([x for x in numbers if x % 2 == 1])
    even = len([x for x in numbers if x % 2 == 0])

    if avg >= 5:
        big_small = "BIG"
    else:
        big_small = "SMALL"

    if odd > even:
        color = "GREEN"
    elif even > odd:
        color = "RED"
    else:
        color = "VIOLET"

    prediction_number = round(avg) % 10

    return big_small, color, prediction_number

# =========================
# GET PREDICTION
# =========================

def get_prediction():

    try:

        data = fetch_data()

        games = data["data"]["list"]

        numbers = []

        for g in games:
            numbers.append(int(g["number"]))

        big_small, color, number = smart_prediction(numbers)

        return {
            "period": games[0]["issueNumber"],
            "prediction": big_small,
            "color": color,
            "number": number,
            "status": "SUCCESS"
        }

    except Exception as e:

        return {
            "period": "-",
            "prediction": "-",
            "color": "-",
            "number": "-",
            "status": str(e)
        }

# =========================
# SAVE RESULT
# =========================

def save_result(result):

    cursor.execute(
        "INSERT INTO stats (result) VALUES (?)",
        (result,)
    )

    conn.commit()

# =========================
# GET STATS
# =========================

def get_stats():

    cursor.execute(
        "SELECT result FROM stats"
    )

    rows = cursor.fetchall()

    wins = 0
    loses = 0

    for r in rows:

        if r[0] == "WIN":
            wins += 1
        else:
            loses += 1

    return wins, loses

# =========================
# START COMMAND
# =========================

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
        ],

        [
            InlineKeyboardButton(
                "📊 Stats",
                callback_data="stats"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 Advanced Prediction Bot Online",
        reply_markup=reply_markup
    )

# =========================
# BUTTON HANDLER
# =========================

async def button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    # =====================
    # PREDICT BUTTON
    # =====================

    if query.data == "predict":

        result = get_prediction()

        text = f"""
🔥 LIVE PREDICTION

📌 Period: {result['period']}

📈 Big/Small: {result['prediction']}
🎨 Color: {result['color']}
🔢 Number: {result['number']}

✅ Status: {result['status']}
"""

        await query.edit_message_text(text)

    # =====================
    # STATS BUTTON
    # =====================

    elif query.data == "stats":

        wins, loses = get_stats()

        text = f"""
📊 BOT STATS

🏆 Wins: {wins}
❌ Loses: {loses}

📈 Total: {wins + loses}
"""

        await query.edit_message_text(text)

# =========================
# /predict COMMAND
# =========================

async def predict(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    result = get_prediction()

    text = f"""
🎯 PREDICTION RESULT

📌 Period: {result['period']}

📈 Big/Small: {result['prediction']}
🎨 Color: {result['color']}
🔢 Number: {result['number']}

✅ Status: {result['status']}
"""

    await update.message.reply_text(text)

# =========================
# AUTO SEND CHANNEL
# =========================

async def auto_prediction():

    while True:

        try:

            result = get_prediction()

            text = f"""
🔥 AUTO SIGNAL

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

        except Exception as e:
            print("AUTO ERROR:", e)

        await asyncio.sleep(60)

# =========================
# MAIN
# =========================

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

# =========================
# RUN BOT
# =========================

if __name__ == "__main__":

    asyncio.run(main())
