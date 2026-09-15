from fastapi import FastAPI

from src.products import routes as products_routes
from src.orders import routes as orders_routes

app = FastAPI()

app.include_router(products_routes.router)
app.include_router(orders_routes.router)
