from azure.cosmos import CosmosClient, PartitionKey
from config import COSMOS_URL, COSMOS_KEY
from datetime import datetime


# -----------------------------
# Cosmos DB Connection
# -----------------------------

client = CosmosClient(COSMOS_URL, COSMOS_KEY)

database = client.create_database_if_not_exists(
    id="price-tracker-db"
)


# -----------------------------
# Containers
# -----------------------------

# Stores tracked products
products_container = database.create_container_if_not_exists(
    id="products",
    partition_key=PartitionKey(path="/id")
)

# Stores price history
price_container = database.create_container_if_not_exists(
    id="price_history",
    partition_key=PartitionKey(path="/product_id")
)


# -----------------------------
# PRODUCT MANAGEMENT
# -----------------------------

def add_product(name, url):
    """
    Add a new product to tracking list
    """

    product_id = name.lower().replace(" ", "-")

    doc = {
        "id": product_id,
        "name": name,
        "url": url,
        "created_at": datetime.utcnow().isoformat(),
        "active": True
    }

    products_container.create_item(doc)

    print(f"Product added → {name}")

    return doc


def get_products():
    """
    Fetch all tracked products
    """

    items = list(products_container.read_all_items())

    products = [
        item for item in items
        if "url" in item
    ]

    return products


def delete_product(product_id):
    """
    Remove product from tracking
    """

    products_container.delete_item(
        item=product_id,
        partition_key=product_id
    )

    print(f"Product removed → {product_id}")


# -----------------------------
# PRICE STORAGE
# -----------------------------

def save_price(product, price):
    """
    Save price snapshot to price_history
    """

    timestamp = datetime.utcnow().isoformat()

    doc = {
        "id": f"{product['id']}_{timestamp}",
        "product_id": product["id"],
        "name": product["name"],
        "price": price,
        "timestamp": timestamp
    }

    price_container.create_item(doc)

    print(f"Saved price for {product['name']} → {price}")


# -----------------------------
# PRICE HISTORY
# -----------------------------

def get_price_history(product_id):
    """
    Fetch price history for a product
    """

    query = f"SELECT * FROM c WHERE c.product_id = '{product_id}' ORDER BY c.timestamp"

    items = list(
        price_container.query_items(
            query=query,
            enable_cross_partition_query=True
        )
    )

    return items


# -----------------------------
# LAST PRICE
# -----------------------------

def get_last_price(product_id):
    """
    Fetch latest recorded price
    """

    query = f"""
    SELECT TOP 1 * FROM c
    WHERE c.product_id = '{product_id}'
    ORDER BY c.timestamp DESC
    """

    items = list(
        price_container.query_items(
            query=query,
            enable_cross_partition_query=True
        )
    )

    return items[0] if items else None