from app.models.user_model import User
from app.models.stock_model import Stock
from app.db import get_db_connection
from flask import session
from datetime import date

class Admin(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def count_total_users(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS cnt FROM user")
                return cursor.fetchone()["cnt"]
        except Exception as e:
            print(f"Error fetching count_total_users: {e}")
            return 0
        finally:
            conn.close()

    def count_active_users(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS cnt FROM user WHERE is_active = 1")
                return cursor.fetchone()["cnt"]
        except Exception as e:
            print(f"Error fetching count_active_users: {e}")
            return 0
        finally:
            conn.close()

    def get_all_users(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT user.*, user_roles.role_name
                    FROM user
                    LEFT JOIN user_roles ON user.role_id = user_roles.role_id
                    ORDER BY user.userID ASC
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all users: {e}")
            return []
        finally:
            conn.close()

    def delete_user(self, target_user_id):
        if int(target_user_id) == int(self.user_id):
            return False
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM user WHERE userID = %s", (target_user_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            conn.close()

    def get_all_funds(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT funds.*, COALESCE(user.first_name, 'System') AS first_name, COALESCE(user.last_name, 'Manager') AS last_name,
                           (SELECT price FROM fund_price_history WHERE fund_id = funds.fund_id ORDER BY date DESC LIMIT 1) AS current_nav
                    FROM funds
                    LEFT JOIN user ON funds.user_id = user.userID
                    ORDER BY funds.fund_id ASC
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all funds: {e}")
            return []
        finally:
            conn.close()

    def add_fund(self, fund_name, fund_theme, strategy, initial_nav=100.0):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO funds (user_id, fund_name, fund_theme, strategy) VALUES (%s, %s, %s, %s)",
                    (self.user_id, fund_name, fund_theme, strategy)
                )
                fund_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO fund_price_history (fund_id, price, date) VALUES (%s, %s, %s)",
                    (fund_id, float(initial_nav), date.today())
                )
                conn.commit()
                return fund_id
        except Exception as e:
            print(f"Error adding fund: {e}")
            return None
        finally:
            conn.close()

    def delete_fund(self, fund_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM funds WHERE fund_id = %s", (fund_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting fund: {e}")
            return False
        finally:
            conn.close()

    def get_all_stocks(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM nasdaq_listed_equities ORDER BY id ASC LIMIT 250")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all stocks: {e}")
            return []
        finally:
            conn.close()

    def add_stock(self, symbol, name, country='United States', sector='Technology', industry='Software'):
        conn = get_db_connection()
        try:
            symbol = symbol.upper().strip()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO nasdaq_listed_equities (symbol, name, country, sector, industry) VALUES (%s, %s, %s, %s, %s)",
                    (symbol, name, country, sector, industry)
                )
                stock_id = cursor.lastrowid
                conn.commit()
            Stock.sync_single_stock_price(stock_id, symbol)
            return stock_id
        except Exception as e:
            print(f"Error adding stock: {e}")
            return None
        finally:
            conn.close()

    def delete_stock(self, stock_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM nasdaq_listed_equities WHERE id = %s", (stock_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting stock: {e}")
            return False
        finally:
            conn.close()

    def toggle_activate_user(self, user_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT is_active FROM user WHERE userID = %s", (user_id,))
                result = cursor.fetchone()
                if result is not None:
                    new_status = 0 if result['is_active'] else 1
                    cursor.execute("UPDATE user SET is_active = %s WHERE userID = %s", (new_status, user_id))
                    conn.commit()
                    return True
                return False
        except Exception as e:
            print(f"Error toggling user status: {e}")
            return False
        finally:
            conn.close()

    def get_all_equity_transactions(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT t.*, u.userID, u.first_name, e.symbol
                    FROM nasdaq_equity_transactions t
                    LEFT JOIN user u ON u.userID = t.user_id
                    LEFT JOIN nasdaq_listed_equities e ON e.id = t.stock_id
                    ORDER BY t.transaction_date DESC
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching equity transactions: {e}")
            return []
        finally:
            conn.close()

    def get_all_fund_transactions(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT ft.*, u.userID, u.first_name, f.fund_name
                    FROM fund_transactions ft
                    LEFT JOIN user u ON u.userID = ft.user_id
                    LEFT JOIN funds f ON f.fund_id = ft.fund_id
                    ORDER BY ft.transaction_date DESC
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching fund transactions: {e}")
            return []
        finally:
            conn.close()

    def get_audit_logs(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT a.*, u.first_name, u.last_name, u.email
                    FROM user_audit a
                    LEFT JOIN user u ON a.user_id = u.userID
                    ORDER BY a.change_date DESC LIMIT 100
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching audit logs: {e}")
            return []
        finally:
            conn.close()

    def get_system_reports(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS cnt, COALESCE(SUM(quantity * price), 0) AS vol FROM nasdaq_equity_transactions")
                eq_stats = cursor.fetchone()
                cursor.execute("SELECT COUNT(*) AS cnt, COALESCE(SUM(quantity * price), 0) AS vol FROM fund_transactions")
                fd_stats = cursor.fetchone()
                cursor.execute("SELECT status, COUNT(*) AS cnt FROM client_orders GROUP BY status")
                order_breakdown = cursor.fetchall()
                return {
                    "equity_tx_count": eq_stats['cnt'],
                    "equity_volume": round(float(eq_stats['vol']), 2),
                    "fund_tx_count": fd_stats['cnt'],
                    "fund_volume": round(float(fd_stats['vol']), 2),
                    "orders": order_breakdown
                }
        except Exception as e:
            print(f"Error generating reports: {e}")
            return {"equity_tx_count": 0, "equity_volume": 0, "fund_tx_count": 0, "fund_volume": 0, "orders": []}
        finally:
            conn.close()

    @staticmethod
    def get_current_user():
        user_id = session.get('user_id')
        if user_id:
            d = Admin.get_user_by_id(user_id)
            if d:
                return Admin(
                    user_id=d["userID"],
                    first_name=d["first_name"],
                    last_name=d["last_name"],
                    email=d["email"],
                    phoneno=d["phone_number"],
                    password=d["password"],
                    role_id=d["role_id"],
                    dob=d["dob"],
                    street=d["street_address"],
                    city=d["city"],
                    state=d["state"],
                    pincode=d["pincode"],
                    country=d["country"],
                    is_active=d["is_active"],
                    created_by=d["created_by"],
                    updated_by=d["updated_by"]
                )
        return None