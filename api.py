import requests
import random
import time
import hashlib
from config import API_URL, HEADERS

def generate_signature():
    return hashlib.md5(str(random.random()).encode()).hexdigest().upper()

def get_game_result():

    payload = {
        "pageSize": 10,
        "pageNo": 1,
        "typeId": 30,
        "language": 0,
        "random": generate_signature(),
        "signature": generate_signature(),
        "timestamp": int(time.time())
    }

    response = requests.post(
        API_URL,
        json=payload,
        headers=HEADERS,
        timeout=15
    )

    data = response.json()

    return data["data"]["list"]