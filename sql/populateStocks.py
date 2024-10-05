import pymysql
from datetime import datetime
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

timeout = 10
conn = pymysql.connect(
    charset=os.getenv('DB_CHARSET'),
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db=os.getenv('DB_NAME'),
    host=os.getenv('DB_HOST'),
    password=os.getenv('DB_PASSWORD'),
    read_timeout=timeout,
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    write_timeout=timeout,
)
  
cur = conn.cursor()

def populate_stock_data_from_csv():
    stock_data = pd.read_csv('sql/stock_data_csv/nasdaq-listed-symbols.csv')
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO nasdaq_listed_equities (symbol, name, country)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            updated_at = CURRENT_TIMESTAMP;
    """   
    for index, row in stock_data.iterrows():
        try:
            cursor.execute(insert_query, (row['Symbol'], row['Company Name'], ''))
        except Exception as e:
            print(f"Error inserting {row['Symbol']}: {e}")
    conn.commit()
    print("POPULATED STOCKS")

if __name__ == '__main__':
    populate_stock_data_from_csv()