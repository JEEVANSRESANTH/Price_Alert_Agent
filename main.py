from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from API.product_routes import router as product_router
from API.price_routes import router as price_router

app = FastAPI(title="AI Price Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Price Tracker API Running"}

app.include_router(product_router)
app.include_router(price_router)