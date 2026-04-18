import pandas as pd
import numpy as np
from db.connection import run_query

def get_sales_prediction():
    df = run_query("""
        SELECT 
            order_date as zi,
            ROUND(SUM(total_amount)::numeric, 2) as vanzari
        FROM orders
        GROUP BY order_date
        ORDER BY order_date
    """)

    df['zi'] = pd.to_datetime(df['zi'])
    df['index_zi'] = (df['zi'] - df['zi'].min()).dt.days

    x = df['index_zi'].values
    y = df['vanzari'].values

    # Regresia liniara
    coef = np.polyfit(x, y, 1)
    poly = np.poly1d(coef)

    # Predictie pentru urmatoarele 30 de zile
    ultima_zi = df['index_zi'].max()
    zile_viitor = np.arange(ultima_zi + 1, ultima_zi + 31)
    date_viitor = [df['zi'].max() + pd.Timedelta(days=int(i - ultima_zi)) for i in zile_viitor]

    df_predictie = pd.DataFrame({
        'zi': date_viitor,
        'vanzari_prezise': poly(zile_viitor).round(2)
    })

    return df, df_predictie, coef