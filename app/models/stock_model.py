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


class Stock:
    def __init__(self, first_name, last_name, email, phoneno, password, role_id=None, dob=None,
                street=None, city=None, state=None, pincode=None, country=None, created_by=None, updated_by=None,
                is_active=False):
        self.first_name = first_name