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
    def __init__(self, fund_id=None, symbol=None, fund_name=None,fund_theme=None, country=None, fund_sector=None, industry=None,strategy=None,Fund_manager=None):
        self.fund_id=fund_id
        self.symbol=symbol
        self.fund_theme=fund_theme
        self.fund_name = fund_name
        self.country = country
        self.fund_sector = fund_sector
        self.industry = industry
        self.strategy=strategy
        self.Fund_manager=Fund_manager

    
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
        
    def add_fund(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO funds (fund_name, fund_theme, fund_sector, strategy, created_by)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.fund_name, self.fund_theme, self.fund_sector, self.strategy, self.created_by))
            conn.commit()
            last_fund_id = self.get_last_fund_id()
            return last_fund_id
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_last_fund_id():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id = cursor.fetchone()[0]
            return last_id
        except Exception as e:
            print(f"Error fetching last fund ID: {e}")
            return None