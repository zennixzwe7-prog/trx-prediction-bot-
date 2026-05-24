from telegram import Bot
from api import get_game_result
from predictor import predict_next
from config import TOKEN, CHAT_ID

import time
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)

last_period = ""

while True:

    try:

        results = get_game_result()

        current = results[0]

        period = current["issueNumber"]

        if period != last_period:

            prediction = predict_next(results)

            message = f"""
🎯 NEW PREDICTION

🆔 Period: {period}

🎨 Color: {prediction['color']}
📈 Size: {prediction['size']}

━━━━━━━━━━━
🤖 AI Prediction Bot
"""

            bot.send_message(
                chat_id=CHAT_ID,
                text=message
            )

            print(message)

            last_period = period

        time.sleep(10)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(5)