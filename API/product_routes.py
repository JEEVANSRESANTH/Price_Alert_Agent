from fastapi import APIRouter
from Services.storage_service import add_product, get_products, delete_product

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def list_products():
    return get_products()


@router.post("/")
def create_product(name: str, url: str):
    return add_product(name, url)


@router.delete("/{product_id}")
def remove_product(product_id: str):
    delete_product(product_id)
    return {"message": "Product removed"}