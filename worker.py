import time
from products import PRODUCTS
from Services.price_service import fetch_price
from Services.alert_service import send_alert
from Services.storage_service import save_price
from config import CHECK_INTERVAL


def run_worker():
    print("🚀 Price Tracker Agent Started...")

    last_prices = {}

    while True:
        for product in PRODUCTS:
            product_id = product["url"]
            name = product["name"]
            url = product["url"]

            try:
                print(f"🔎 Checking {name}")

                price = fetch_price(url)

                if price is None:
                    continue

                # First run
                if product_id not in last_prices:
                    send_alert(f"📦 {name}\nInitial Price: ₹{price}")
                    last_prices[product_id] = price
                    save_price(product, price)
                    continue

                # Price changed
                if price != last_prices[product_id]:
                    send_alert(
                        f"🔔 Price Change Detected!\n"
                        f"📦 {name}\n"
                        f"Old Price: ₹{last_prices[product_id]}\n"
                        f"New Price: ₹{price}"
                    )
                    last_prices[product_id] = price
                    save_price(product, price)

                time.sleep(90)  # prevent Apify rate limit

            except Exception as e:
                print(f"❌ Error processing {name}: {e}")

        print("⏳ Sleeping...")
        time.sleep(CHECK_INTERVAL)