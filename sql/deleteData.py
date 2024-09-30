import pymysql
from datetime import datetime
import os 
from dotenv import load_dotenv

load_dotenv()

timeout = 10


def delete_all_data_from_tables():
    try:
        conn = pymysql.connect(
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
        cursor = conn.cursor()

        # Step 1: Retrieve all table names from the AMS_DB
        query_get_tables = """
        SELECT table_name 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE table_schema = 'AMS_DB'
        """

        cursor.execute(query_get_tables)
        tables = cursor.fetchall()
        
        # Step 2: Disable foreign key checks to avoid constraint issues
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        # Step 3: Delete data from each table
        for table in tables:
            print(table["TABLE_NAME"])
            table_name = table['TABLE_NAME']
            delete_query = f"DELETE FROM {table_name};"
            cursor.execute(delete_query)
            print(f"Deleted all data from {table_name}")

        # Step 4: Enable foreign key checks back
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        # Commit the changes
        conn.commit()

        # Close connection
        conn.close()
        
        print("All data deleted from all tables successfully.")

    except Exception as e:
        print(f"Error while deleting data: {e}")
        if conn:
            conn.rollback()  # Roll back if there is an error
            conn.close()

if __name__ == "__main__":
    delete_all_data_from_tables()