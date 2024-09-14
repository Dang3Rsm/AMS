import mysql.connector
# just a template we have to implement it from scratch
class MySQLModel:
    def __init__(self):
        self.conn = mysql.connector.connect( # load from env ( do not commit the envs)
            host='localhost',
            user='root',
            password='password',
            database='flask_db'
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()


class User(MySQLModel):
    def __init__(self):
        super().__init__()

    def create_user(self, username, email):
        query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        self.cursor.execute(query, (username, email))
        self.conn.commit()

    def get_all_users(self):
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_user(self, user_id, new_email):
        query = "UPDATE users SET email = %s WHERE id = %s"
        self.cursor.execute(query, (new_email, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = %s"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()
