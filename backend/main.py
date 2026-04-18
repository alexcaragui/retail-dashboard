import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from backend.routers import sales, customers, inventory

app = FastAPI(title="Retail Dashboard API", version="1.0.0")

app.include_router(sales.router, prefix="/api/sales", tags=["Sales"])
app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Retail Dashboard API functioneaza!"}