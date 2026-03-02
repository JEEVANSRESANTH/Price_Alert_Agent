from Services.price_service import fetch_price

url = "https://www.amazon.in/s?k=iphone+17+pro+max"

price = fetch_price(url)

print("Fetched price:", price)