import pymysql
import os 
from dotenv import load_dotenv

load_dotenv()
timeout = 10

# just a template we have to implement it from scratch
class AMS_DB:
    def __init__(self):
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
    def __init__(self):
        super().__init__()

    def create_user(self, username, email):
        # query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        # self.cursor.execute(query, (username, email))
        # self.conn.commit()
        pass

    def get_all_users(self):
        # query = "SELECT * FROM users"
        # self.cursor.execute(query)
        # return self.cursor.fetchall()
        pass

    def update_user(self, user_id, new_email):
        # query = "UPDATE users SET email = %s WHERE id = %s"
        # self.cursor.execute(query, (new_email, user_id))
        # self.conn.commit()
        pass

    def delete_user(self, user_id):
        # query = "DELETE FROM users WHERE id = %s"
        # self.cursor.execute(query, (user_id,))
        # self.conn.commit()
        pass
