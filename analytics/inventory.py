from db.connection import run_query

def get_low_stock():
    return run_query("""
        SELECT 
            name as produs,
            category as categorie,
            stock_quantity as stoc_curent,
            reorder_level as nivel_minim
        FROM products
        WHERE stock_quantity <= reorder_level
        ORDER BY stock_quantity ASC
    """)

def get_all_stock():
    return run_query("""
        SELECT 
            name as produs,
            category as categorie,
            stock_quantity as stoc_curent,
            reorder_level as nivel_minim,
            price as pret
        FROM products
        ORDER BY stock_quantity ASC
    """)

def get_stock_rotation():
    return run_query("""
        SELECT 
            p.name as produs,
            p.stock_quantity as stoc_curent,
            COALESCE(SUM(oi.quantity), 0) as total_vandut
        FROM products p
        LEFT JOIN order_items oi ON oi.product_id = p.id
        GROUP BY p.name, p.stock_quantity
        ORDER BY total_vandut DESC
    """)