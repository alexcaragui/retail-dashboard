from fastapi import APIRouter
from db.connection import run_query

router = APIRouter()

@router.get("/low-stock")
def low_stock():
    df = run_query("""
        SELECT 
            name as produs,
            category as categorie,
            stock_quantity as stoc_curent,
            reorder_level as nivel_minim
        FROM products
        WHERE stock_quantity <= reorder_level
        ORDER BY stock_quantity ASC
    """)
    return df.to_dict(orient='records')

@router.get("/all")
def all_stock():
    df = run_query("""
        SELECT 
            name as produs,
            category as categorie,
            stock_quantity as stoc_curent,
            reorder_level as nivel_minim,
            price as pret
        FROM products
        ORDER BY stock_quantity ASC
    """)
    return df.to_dict(orient='records')

@router.get("/rotation")
def stock_rotation():
    df = run_query("""
        SELECT 
            p.name as produs,
            p.stock_quantity as stoc_curent,
            COALESCE(SUM(oi.quantity), 0) as total_vandut
        FROM products p
        LEFT JOIN order_items oi ON oi.product_id = p.id
        GROUP BY p.name, p.stock_quantity
        ORDER BY total_vandut DESC
    """)
    return df.to_dict(orient='records')