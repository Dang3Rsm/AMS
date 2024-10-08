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
    
    @staticmethod
    def search_funds(search_query):
        # Prepare the SQL query with placeholders
        conn = get_db_connection()
        sql_query = """
        SELECT * FROM funds 
        WHERE LOWER(fund_name) LIKE LOWER(%s) 
        """
        
        # Format the query input with wildcards
        query_input = f'%{search_query}%'  # Escape the user input
        try:
            with conn.cursor() as cursor:
                # Execute the query with the input parameters
                cursor.execute(sql_query, (query_input, ))
                funds = cursor.fetchall()  # Fetch all matching records
                return funds  # Return the results
        except Exception as e:
            print(f"Error during database operation: {e}")
            return []  # Return an empty list on error
        finally:
            conn.close()  # Ensure the connection is closed
