import time

from Services.price_service import fetch_price
from Services.alert_service import send_alert
from Services.storage_service import save_price, get_products
from config import CHECK_INTERVAL


def run_worker():

    print("🚀 Price Tracker Agent Started...")

    last_prices = {}

    while True:

        # Load products dynamically from Cosmos DB
        products = get_products()

        for product in products:

            name = product["name"]
            url = product["url"]

            try:
                print(f"🔎 Checking {name}")

                price = fetch_price(url)

                if price is None:
                    continue

                # First time seeing this product
                if url not in last_prices:

                    send_alert(
                        f"""📦 PRODUCT TRACKING STARTED

{name}

Initial Price: ₹{price}
"""
                    )

                    last_prices[url] = price
                    save_price(product, price)
                    continue

                old_price = last_prices[url]

                # Detect price drop
                if price < old_price:

                    drop = old_price - price
                    percent = (drop / old_price) * 100

                    send_alert(
                        f"""🔥 PRICE DROP ALERT

{name}

Old Price: ₹{old_price}
New Price: ₹{price}

Drop: ₹{drop} ({percent:.2f}%)
"""
                    )

                    save_price(product, price)

                # Always update last seen price
                last_prices[url] = price

            except Exception as e:
                print("Error:", e)

        print("Sleeping...")
        time.sleep(CHECK_INTERVAL)