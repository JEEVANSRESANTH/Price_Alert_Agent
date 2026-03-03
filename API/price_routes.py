from fastapi import APIRouter
from Services.storage_service import get_price_history, get_last_price

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/history/{product_id}")
def price_history(product_id: str):
    return get_price_history(product_id)


@router.get("/last/{product_id}")
def last_price(product_id: str):
    return get_last_price(product_id)