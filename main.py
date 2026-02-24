import requests
import time
BOT_TOKEN = "8763912797:AAFJJ7PZpEFScX4iMSf1G_cMNMP_vtiQogo"
CHAT_ID = "6332098727"

URL = "https://real-time-amazon-data.p.rapidapi.com/product-details"

querystring = {
    "asin": "B07ZPKBL9V",
    "country": "US"
}

headers = {
    "X-RapidAPI-Key": "ebdfc10291msh8b2beab858db5bcp150a5djsn8ce0e0f73d61",
    "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
}

TARGET_PRICE = 99999

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=payload)


def get_price():
    try:
        r = requests.get(URL, headers=headers, params=querystring)
        data = r.json()

        if "data" not in data:
            print("API temporary issue")
            return None

        price_text = data["data"].get("product_price")

        if not price_text:
            return None

        price = float(price_text.replace("$","").replace(",",""))
        return price

    except Exception as e:
        print("Error:", e)
        return None

while True:
    price = get_price()

    if price:
        print("Current price:", price)

        if price < TARGET_PRICE:
            message = f"🔥 Price dropped!\nCurrent price: {price}"
            send_telegram(message)

    print("Checking again in 5 min...\n")
    time.sleep(300)