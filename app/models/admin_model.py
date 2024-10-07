from app.models.user_model import User
from app.db import get_db_connection
from flask import session

class Admin(User):
    def __init__(self, user_id=None, first_name=None, last_name=None, email=None, phoneno=None, password=None, role_id=None, dob=None,
                 street=None, city=None, state=None, pincode=None, country=None, created_by=None, updated_by=None,
                 is_active=False):
        super().__init__(user_id, first_name, last_name, email, phoneno, password, role_id, dob,
                         street, city, state, pincode, country, created_by, updated_by, is_active)


    def count_total_users(self):
        """Count of total users"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = """
                    SELECT COUNT(*) FROM user
            """
            cursor.execute(query)
            total_users = cursor.fetchone()["COUNT(*)"]
            return total_users
        except Exception as e:
            print(f"Error fetching count_total_users: {e}")
            return -1

    def count_active_users(self):
        """Count of total users"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = """
                    SELECT COUNT(*) FROM user WHERE is_active = 1
            """
            cursor.execute(query)
            active_users = cursor.fetchone()["COUNT(*)"]
            return active_users
        except Exception as e:
            print(f"Error fetching count_active_users: {e}")
            return -1
        
    # Admin-specific methods
    def get_all_users(self):
        """Admin can get all users."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT user.*, user_roles.role_name
                FROM user
                LEFT JOIN user_roles ON user.role_id = user_roles.role_id
            """
            cursor.execute(query)
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error fetching all users: {e}")
            return None

    def deactivate_user(self, user_id):
        """Admin can deactivate a user account."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "UPDATE user SET is_active = 0 WHERE userID = %s"
            cursor.execute(query, (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deactivating user {user_id}: {e}")
            return False

    def promote_to_admin(self, user_id):
        """Admin can promote a user to an admin role."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # Assuming '1' is the role_id for Admin
            query = "UPDATE user SET role_id = 1 WHERE userID = %s"
            cursor.execute(query, (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error promoting user {user_id} to admin: {e}")
            return False

    def get_all_orders(self):
        """Admin can view all client orders."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM client_orders"
            cursor.execute(query)
            orders = cursor.fetchall()
            return orders
        except Exception as e:
            print(f"Error fetching all orders: {e}")
            return None

    def get_all_equity_transactions(self):
        """Admin can view all client transactions."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM nasdaq_equity_transactions"
            cursor.execute(query)
            equity_transactions = cursor.fetchall()
            return equity_transactions
        except Exception as e:
            print(f"Error fetching all get_all_equity_transactions(): {e}")
            return None
        
    def get_all_fund_transactions(self):
        """Admin can view all fund transactions."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM fund_transactions"
            cursor.execute(query)
            fund_transactions = cursor.fetchall()
            return fund_transactions
        except Exception as e:
            print(f"Error fetching all get_all_fund_transactions(): {e}")
            return None
        
    @staticmethod
    def get_current_user():
        user_id = session.get('user_id')
        if user_id:
            d =  Admin.get_user_by_id(user_id)
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
            else:
                print("error at get_user_by_id()")
        print("error at get_current_user()")
        return None
