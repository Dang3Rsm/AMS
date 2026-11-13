from app.db import get_db_connection

class Fund:
    def __init__(self, fund_id, fund_name=None, fund_theme=None, strategy=None):
        self.fund_id = fund_id
        self.fund_name = fund_name
        self.fund_theme = fund_theme
        self.strategy = strategy

    @staticmethod
    def get_fund_by_id(fund_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM funds WHERE fund_id = %s", (fund_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def search_funds(search_query):
        conn = get_db_connection()
        sql_query = """
            SELECT * FROM funds 
            WHERE LOWER(fund_name) LIKE LOWER(%s) OR LOWER(fund_theme) LIKE LOWER(%s)
        """
        query_input = f'%{search_query}%'
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_query, (query_input, query_input))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error during database operation: {e}")
            return []
        finally:
            conn.close()