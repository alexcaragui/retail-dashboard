import pandas as pd
import random
from datetime import datetime, timedelta
from sqlalchemy import text
import sys
sys.path.append('..')
from db.connection import engine

random.seed(42)

# --- Produse ---
categorii = ['Electronice', 'Haine', 'Alimente', 'Sport', 'Casa']
produse = [
    ('Laptop Pro', 'Electronice', 3500, 45, 10),
    ('Telefon Smart', 'Electronice', 2200, 80, 15),
    ('Tricou Basic', 'Haine', 89, 200, 30),
    ('Pantofi Sport', 'Sport', 350, 60, 20),
    ('Cafea Premium', 'Alimente', 55, 15, 25),
    ('Tastatura Wireless', 'Electronice', 280, 90, 20),
    ('Geaca Iarna', 'Haine', 450, 40, 10),
    ('Ulei Masline', 'Alimente', 35, 8, 30),
    ('Haltera 10kg', 'Sport', 120, 55, 15),
    ('Perna Memory Foam', 'Casa', 195, 70, 20),
    ('Casti Audio', 'Electronice', 520, 35, 10),
    ('Jeans Slim', 'Haine', 180, 110, 25),
    ('Proteina Zer', 'Sport', 210, 12, 20),
    ('Lampa LED', 'Casa', 95, 85, 15),
    ('Biscuiti Bio', 'Alimente', 18, 5, 40),
]

# --- Clienti ---
nume_clienti = [
    'Andrei Popescu', 'Maria Ionescu', 'Ion Popa', 'Elena Dumitrescu',
    'Alexandru Radu', 'Ioana Constantin', 'Mihai Gheorghe', 'Ana Stoica',
    'Cristian Marin', 'Laura Petrescu', 'Bogdan Stancu', 'Alina Dinu',
    'Florin Matei', 'Roxana Tudor', 'Catalin Vlad', 'Diana Moldovan',
    'Razvan Luca', 'Simona Barbu', 'Adrian Rusu', 'Georgiana Neagu'
]

orase = ['București', 'Cluj-Napoca', 'Timișoara', 'Iași', 'Brașov', 'Craiova']

def genereaza_email(nume):
    parts = nume.lower().split()
    return f"{parts[0]}.{parts[1]}@email.com"

def data_random(zile_inapoi=365):
    start = datetime.now() - timedelta(days=zile_inapoi)
    return start + timedelta(days=random.randint(0, zile_inapoi))

print("Se sterg datele vechi...")
with engine.connect() as conn:
    conn.execute(text("TRUNCATE order_items, orders, customers, products RESTART IDENTITY CASCADE"))
    conn.commit()

print("Se insereaza produsele...")
with engine.connect() as conn:
    for p in produse:
        conn.execute(text("""
            INSERT INTO products (name, category, price, stock_quantity, reorder_level)
            VALUES (:name, :category, :price, :stock, :reorder)
        """), {"name": p[0], "category": p[1], "price": p[2], "stock": p[3], "reorder": p[4]})
    conn.commit()

print("Se insereaza clientii...")
customer_ids = []
with engine.connect() as conn:
    for i, nume in enumerate(nume_clienti):
        data_creare = data_random(500)
        is_returning = i % 3 != 0
        conn.execute(text("""
            INSERT INTO customers (name, email, city, created_at, is_returning)
            VALUES (:name, :email, :city, :created_at, :is_returning)
        """), {
            "name": nume,
            "email": genereaza_email(nume),
            "city": random.choice(orase),
            "created_at": data_creare.date(),
            "is_returning": is_returning
        })
    conn.commit()

    result = conn.execute(text("SELECT id FROM customers ORDER BY id"))
    customer_ids = [row[0] for row in result]

print("Se insereaza comenzile...")
with engine.connect() as conn:
    result = conn.execute(text("SELECT id, price FROM products ORDER BY id"))
    products_db = [(row[0], row[1]) for row in result]

    for _ in range(300):
        customer_id = random.choice(customer_ids)
        order_date = data_random(365)
        nr_produse = random.randint(1, 4)
        produse_alese = random.sample(products_db, nr_produse)

        total = sum(p[1] * random.randint(1, 3) for p in produse_alese)

        result = conn.execute(text("""
            INSERT INTO orders (customer_id, order_date, total_amount, status)
            VALUES (:cid, :date, :total, 'completed')
            RETURNING id
        """), {"cid": customer_id, "date": order_date.date(), "total": total})
        order_id = result.fetchone()[0]

        for prod_id, prod_price in produse_alese:
            qty = random.randint(1, 3)
            conn.execute(text("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                VALUES (:oid, :pid, :qty, :price)
            """), {"oid": order_id, "pid": prod_id, "qty": qty, "price": prod_price})

    conn.commit()

print("Date generate cu succes! 300 comenzi, 20 clienti, 15 produse.")