from app.db import get_db_connection

import pymysql

# This is to solve the connection problem
# import os
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


class User:
    def __init__(self, first_name, last_name, email, phoneno, password, role_id=None, dob=None,
                street=None, city=None, state=None, pincode=None, country=None, created_by=None, updated_by=None,
                is_active=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role_id = role_id
        self.phoneno = phoneno
        self.dob = dob
        self.street = street
        self.city = city
        self.state = state
        self.pincode = pincode
        self.country = country
        self.is_active = is_active
        self.created_by = created_by
        self.updated_by = updated_by

    def register_user(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO user (first_name, last_name, email, password, role_id, phone_number, dob, street_address, city, state, pincode, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.first_name, self.last_name, self.email, self.password, self.role_id, self.phoneno, self.dob, self.street, self.city, self.state, self.pincode, self.country))
            conn.commit()
            last_user_id = User.get_last_userID()
            query = f"UPDATE user SET created_by = {last_user_id}, updated_by = {last_user_id} WHERE userID = {last_user_id}"
            cursor.execute(query)
            conn.commit()
            action = "INSERT"
            field_changed = "created_by"
            audit_query = f"INSERT INTO user_audit (user_id, action, field_changed, new_value) VALUES ({last_user_id}, 'INSERT', 'created_by', {last_user_id}); "
            cursor.execute(audit_query)
            conn.commit()
            return last_user_id
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM user"
            cursor.execute(query)
            users = cursor.fetchall()
            conn.close()
            return users
        except Exception as e:
            print(f"Error: {e}")
            return None


    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            conn.close()
            return user
        except Exception as e:
            print(f"Error: {e}")
            return None


    @staticmethod
    def get_roles():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_roles")
            roles = cursor.fetchall()
            return roles
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    @staticmethod
    def get_role_by_id():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT role_name FROM user_roles WHERE role_id = %s")
            role_id = cursor.fetchone()
            if role_id:
                return role_id[0]
            else:
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        

    @staticmethod
    def get_last_userID():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(userID) FROM user")
            last_uid = cursor.fetchone()
            if last_uid:
                return last_uid["MAX(userID)"]
            else:
                return None
        except Exception as e:
            print(f"Error at get_last_userID(): {e}")
            return None
