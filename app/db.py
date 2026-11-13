from flask import current_app
import pymysql


def get_db_connection():
    conn = pymysql.connect(
        charset             =            current_app.config['DB_CHARSET'],
        connect_timeout     =            current_app.config['DB_CONNECT_TIMEOUT'],
        cursorclass         =            pymysql.cursors.DictCursor,
        db                  =            current_app.config['DB_NAME'],
        host                =            current_app.config['DB_HOST'],
        password            =            current_app.config['DB_PASSWORD'],
        read_timeout        =            current_app.config['DB_READ_TIMEOUT'],
        port                =            current_app.config['DB_PORT'],
        user                =            current_app.config['DB_USER'],
        write_timeout       =            current_app.config['DB_WRITE_TIMEOUT'],
    )
    return conn