import requests
from config import BOT_TOKEN, CHAT_ID


def send_alert(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code != 200:
            print("Telegram error:", response.text)

    except Exception as e:
        print("Telegram send failed:", e)