from azure.cosmos import CosmosClient
from config import COSMOS_URL, COSMOS_KEY
from datetime import datetime

client = CosmosClient(COSMOS_URL, COSMOS_KEY)

database = client.create_database_if_not_exists(id="price-tracker-db")

container = database.create_container_if_not_exists(
    id="products",
    partition_key={"path": "/id"}
)

def save_price(product, price):

    timestamp = datetime.utcnow().isoformat()

    doc = {
        "id": f"{product['name']}_{timestamp}",
        "name": product["name"],
        "price": price,
        "timestamp": timestamp
    }

    container.create_item(doc)

    print(f"Saved price for {product['name']} → {price}")