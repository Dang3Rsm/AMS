from app.db import get_db_connection
import pandas as pd
import yfinance as yf
import logging
# This is to solve the connection problem
# import os
# import pymysql
# timeout = 10
# def get_db_connection():
#     conn = pymysql.connect(
#         charset=os.getenv('DB_CHARSET'),
#         connect_timeout=timeout,
#         cursorclass=pymysql.cursors.DictCursor,
#         db=os.getenv('DB_NAME'),
#         host=os.getenv('DB_HOST'),
#         password=os.getenv('DB_PASSWORD'),
#         read_timeout=timeout,
#         port=int(os.getenv('DB_PORT')),
#         user=os.getenv('DB_USER'),
#         write_timeout=timeout,
#     )
#     return conn


class Stock:
    def __init__(self, stock_id=None, symbol=None, name=None, country=None, sector=None, industry=None):
        self.stock_id = stock_id
        self.symbol = symbol
        self.name = name
        self.country = country
        self.sector = sector
        self.industry = industry
    
    @staticmethod
    def get_stock_by_id(stock_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM nasdaq_listed_equities WHERE stock_id = %s"
            cursor.execute(query, (stock_id,))
            stock = cursor.fetchone()
            conn.close()
            return stock
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_stockID_by_symbol(symbol): 
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT id FROM nasdaq_listed_equities WHERE symbol = %s"
            cursor.execute(query, (symbol,))
            stock = cursor.fetchone()
            conn.close()
            return stock[0] if stock else None
        except Exception as e:
            print(f"Error at get_stockID_by_symbol(symbol): {e}")
            return None

    
    @staticmethod
    def fetch_stock_data():
        logging.info("fetch_stock_data is running.")
        print("RUNNING fetch_stock_data")
        conn = get_db_connection()
        
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT stock_id FROM watchlist")
            stock_ids = [row['stock_id'] for row in cursor.fetchall()]

            for stock_id in stock_ids:
                try:
                    cursor.execute("SELECT symbol FROM nasdaq_listed_equities WHERE id = %s", (stock_id,))
                    symbol_row = cursor.fetchone()
                    if symbol_row:
                        symbol = symbol_row["symbol"]
                        stock = yf.Ticker(symbol)
                        stock_data = stock.history(period="5d", interval="1d")
                        if not stock_data.empty:
                            row = stock_data.iloc[0]
                            price_date = row.name.date()
                            open_price = row['Open']
                            close_price = row['Close']
                            high_price = row['High']
                            low_price = row['Low']
                            volume = row['Volume']
                            cursor.execute("""
                                SELECT close_price FROM equity_price_history 
                                WHERE stock_id = %s 
                                ORDER BY price_date DESC LIMIT 1
                            """, (stock_id,))
                            last_close_row = cursor.fetchone()
                            if last_close_row:
                                last_close_price = float(last_close_row["close_price"])
                                if last_close_price != 0:
                                    percent_change = ((close_price - last_close_price) / last_close_price) * 100
                                else:
                                    percent_change = None
                            else:
                                percent_change = None

                            insert_query = """
                                INSERT INTO equity_price_history (stock_id, price_date, open_price, close_price, high_price, low_price, volume, percent_change)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                ON DUPLICATE KEY UPDATE
                                    open_price = VALUES(open_price),
                                    close_price = VALUES(close_price),
                                    high_price = VALUES(high_price),
                                    low_price = VALUES(low_price),
                                    volume = VALUES(volume),
                                    percent_change = VALUES(percent_change);
                            """
                            cursor.execute(insert_query, (stock_id, price_date, open_price, close_price, high_price, low_price, volume, percent_change))
                            conn.commit()
                        else:
                            logging.warning(f"No data fetched for symbol: {symbol}")
                    else:
                        logging.warning(f"No symbol found for stock_id: {stock_id}")
                except Exception as e:
                    logging.error(f"Error fetching data for stock_id {stock_id}: {e}")

            cursor.close()
            conn.close()