from app.db import get_db_connection

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


class Fund:
    def __init__(self, fund_id, symbol=None, name=None, country=None, sector=None, industry=None):
        self.fund_id = fund_id
        self.symbol = symbol
        self.name = name
        self.country = country
        self.sector = sector
        self.industry = industry
    
    @staticmethod
    def get_fund_by_id(fund_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM nasdaq_listed_equities WHERE fund_id = %s"
            cursor.execute(query, (fund_id,))
            fund = cursor.fetchone()
            conn.close()
            return fund
        except Exception as e:
            print(f"Error: {e}")
            return None