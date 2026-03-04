from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from API.product_routes import router as product_router
from API.price_routes import router as price_router

app = FastAPI(title="AI Price Tracker API")

# -------------------------------
# CORS CONFIG
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://.*azurecontainerapps.io",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# API ROUTES
# -------------------------------

app.include_router(product_router)
app.include_router(price_router)

# -------------------------------
# SERVE UI (Dashboard)
# -------------------------------

app.mount("/", StaticFiles(directory="UI", html=True), name="ui")