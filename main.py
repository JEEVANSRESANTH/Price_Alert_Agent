
import requests
import time
from dotenv import load_dotenv
import os

# load env variables
load_dotenv(dotenv_path=".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

URL = "https://real-time-amazon-data.p.rapidapi.com/product-details"

querystring = {
    "asin": "B07ZPKBL9V",
    "country": "US"
}

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
}

TARGET_PRICE = 99999


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    r = requests.post(url, data=payload)
    


def get_price():
    try:
        r = requests.get(URL, headers=headers, params=querystring, timeout=10)
        data = r.json()

        if "data" not in data:
            return None

        price_text = data["data"].get("product_price")

        if not price_text:
            return None

        price = float(price_text.replace("$", "").replace(",", ""))
        return price

    except Exception:
        return None


last_price = None

MIN_REASONABLE_PRICE = 200   # ignore unrealistic prices


try:
    while True:

        price = None
        for _ in range(3):
            price = get_price()
            if price is not None:
                break
            time.sleep(5)

        if price is None:
            print("API issue — retrying\n")
            time.sleep(60)
            continue

        # ignore unrealistic price
        if price < MIN_REASONABLE_PRICE:
            print(f"Ignoring suspicious price: {price}")
            time.sleep(300)
            continue

        # first run → send alert
        if last_price is None:
            last_price = price
            print(f"Current price: {price}")
            send_telegram(f"Initial price: {price}")

        # price changed → send alert
        elif price != last_price:
            print(f"Price changed: {last_price} → {price}")
            send_telegram(f"Price changed: {last_price} → {price}")
            last_price = price

        else:
            print(f"No change — {price}")

        time.sleep(300)

except KeyboardInterrupt:
    print("Agent stopped 👋")