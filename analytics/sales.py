from db.connection import run_query

def get_total_sales():
    return run_query("""
        SELECT ROUND(SUM(total_amount)::numeric, 2) as total
        FROM orders
    """)

def get_monthly_sales():
    return run_query("""
        SELECT 
            TO_CHAR(order_date, 'YYYY-MM') as luna,
            ROUND(SUM(total_amount)::numeric, 2) as vanzari
        FROM orders
        GROUP BY luna
        ORDER BY luna
    """)

def get_top_products():
    return run_query("""
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

def get_daily_sales_last_30():
    return run_query("""
        SELECT 
            order_date as zi,
            ROUND(SUM(total_amount)::numeric, 2) as vanzari
        FROM orders
        WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY order_date
        ORDER BY order_date
    """)