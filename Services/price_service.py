import requests
from bs4 import BeautifulSoup
from config import MIN_REASONABLE_PRICE

def fetch_price(product_url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-IN,en;q=0.9"
    }

    try:
        response = requests.get(product_url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Request failed:", response.status_code)
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # multiple price selectors
        price_tag = soup.select_one(
            "#priceblock_ourprice, #priceblock_dealprice, .a-price-whole, .a-price span.a-offscreen"
        )

        if not price_tag:
            print("Price not found")
            return None

        price = price_tag.text.replace("₹","").replace(",","").strip()

        price = float(price)

        if price < MIN_REASONABLE_PRICE:
            return None

        return price

    except Exception as e:
        print("Scraper error:", e)
        return None