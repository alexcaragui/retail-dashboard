from sqlalchemy import create_engine
import pandas as pd

DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/retail_dashboard"

engine = create_engine(DATABASE_URL)

def get_connection():
    return engine.connect()

def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(query, conn)