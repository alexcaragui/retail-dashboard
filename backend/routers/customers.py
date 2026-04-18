from fastapi import APIRouter
from db.connection import run_query

router = APIRouter()

@router.get("/new-vs-returning")
def new_vs_returning():
    df = run_query("""
        SELECT 
            CASE WHEN is_returning THEN 'Recurenti' ELSE 'Noi' END as tip,
            COUNT(*) as numar
        FROM customers
        GROUP BY is_returning
    """)
    return df.to_dict(orient='records')

@router.get("/top")
def top_customers():
    df = run_query("""
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
    return df.to_dict(orient='records')

@router.get("/by-city")
def customers_by_city():
    df = run_query("""
        SELECT 
            city as oras,
            COUNT(*) as numar_clienti
        FROM customers
        GROUP BY city
        ORDER BY numar_clienti DESC
    """)
    return df.to_dict(orient='records')