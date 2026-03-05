import requests
from bs4 import BeautifulSoup
import random
from config import MIN_REASONABLE_PRICE


def fetch_price(product_url):

    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64)"
        ]),
        "Accept-Language": "en-IN,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(product_url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Request failed:", response.status_code)
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Amazon price selectors
        selectors = [
            ".a-price-whole",
            ".a-offscreen",
            "#priceblock_ourprice",
            "#priceblock_dealprice"
        ]

        price_text = None

        for selector in selectors:
            tag = soup.select_one(selector)
            if tag:
                price_text = tag.text
                break

        if not price_text:
            print("Price not found")
            return None

        price = price_text.replace("₹", "").replace(",", "").strip()

        price = float(price)

        if price < MIN_REASONABLE_PRICE:
            return None

        return price

    except Exception as e:
        print("Scraper error:", e)
        return None