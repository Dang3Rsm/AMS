import pymysql
import os 
from dotenv import load_dotenv

load_dotenv()
timeout = 10

# CRUD functions for the user table
class AMS_DB:
    def _init_(self):
        self.conn = pymysql.connect(
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
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()


class User(AMS_DB):
    def _init_(self):
        super()._init_()

    def create_user(self, first_name,
                    last_name, email,
                    password, role_id,
                    phone_number, dob,
                    street_address, city, 
                    state, pincode, country, 
                    created_by):
        try:
            query = """
                INSERT INTO user (first_name, last_name, 
                email, password, 
                role_id, phone_number, 
                dob, street_address, city, 
                state, pincode, country, 
                created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, 
                      email, password, role_id, 
                      phone_number, dob, 
                      street_address, city, 
                      state, pincode, country, 
                      created_by)
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.lastrowid
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        

    def get_user_by_id(self, user_id):
        try:
            query = "SELECT * FROM user WHERE userID = %s"
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            return result
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        

    def update_user(self, user_id, **kwargs):
        try:
            set_clause = ', '.join([f"{k} = %s" for k in kwargs.keys()])
            query = f"UPDATE user SET {set_clause}, updated_At = CURRENT_TIMESTAMP WHERE userID = %s"
            values = list(kwargs.values()) + [user_id]
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.rowcount
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        

    def delete_user(self, userId):
        try:
            query = "DELETE FROM users WHERE id = %s"
            self.cursor.execute(query, (userId,))
            self.conn.commit()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        

    def get_all_users(self):
        try:
            query = "SELECT * FROM user"
            self.cursor.execute(query)
        except pymysql.MySQLError as e:
            print(f"Error: {e}")