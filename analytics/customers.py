from db.connection import run_query

def get_new_vs_returning():
    return run_query("""
        SELECT 
            CASE WHEN is_returning THEN 'Recurenti' ELSE 'Noi' END as tip,
            COUNT(*) as numar
        FROM customers
        GROUP BY is_returning
    """)

def get_top_customers():
    return run_query("""
        SELECT 
            c.name as client,
            c.city as oras,
            COUNT(o.id) as nr_comenzi,
            ROUND(SUM(o.total_amount)::numeric, 2) as total_cheltuit
        FROM customers c
        JOIN orders o ON o.customer_id = c.id
        GROUP BY c.name, c.city
        ORDER BY total_cheltuit DESC
        LIMIT 10
    """)

def get_customers_by_city():
    return run_query("""
        SELECT 
            city as oras,
            COUNT(*) as numar_clienti
        FROM customers
        GROUP BY city
        ORDER BY numar_clienti DESC
    """)