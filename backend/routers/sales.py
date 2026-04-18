from fastapi import APIRouter
from db.connection import run_query

router = APIRouter()

@router.get("/total")
def total_sales():
    df = run_query("""
        SELECT ROUND(SUM(total_amount)::numeric, 2) as total
        FROM orders
    """)
    return {"total": float(df['total'].iloc[0])}

@router.get("/monthly")
def monthly_sales():
    df = run_query("""
        SELECT 
            TO_CHAR(order_date, 'YYYY-MM') as luna,
            ROUND(SUM(total_amount)::numeric, 2) as vanzari
        FROM orders
        GROUP BY luna
        ORDER BY luna
    """)
    return df.to_dict(orient='records')

@router.get("/top-products")
def top_products():
    df = run_query("""
        SELECT 
            p.name as produs,
            SUM(oi.quantity) as cantitate_vanduta,
            ROUND(SUM(oi.quantity * oi.unit_price)::numeric, 2) as venit
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        GROUP BY p.name
        ORDER BY venit DESC
        LIMIT 5
    """)
    return df.to_dict(orient='records')

@router.get("/daily-last-30")
def daily_last_30():
    df = run_query("""
        SELECT 
            order_date::text as zi,
            ROUND(SUM(total_amount)::numeric, 2) as vanzari
        FROM orders
        WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY order_date
        ORDER BY order_date
    """)
    return df.to_dict(orient='records')