from app.db import get_db_connection
from flask import session
from ..security import check_password
# This is to solve the connection problem
# import os
# import pymysql
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
    def __init__(self, user_id = None, first_name=None, last_name=None, email=None, phoneno=None, password=None, role_id=None, dob=None,
                street=None, city=None, state=None, pincode=None, country=None, created_by=None, updated_by=None,
                is_active=False):
        self.userData = None
        self.user_id = user_id
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
        self.darkMode = User.get_user_darkMode(user_id=user_id)

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
            action = 'INSERT'
            field_changed = 'created_by'
            audit_query = f"INSERT INTO user_audit (user_id, action, field_changed, new_value) VALUES ({last_user_id}, {action}, {field_changed}, {last_user_id}); "
            cursor.execute(audit_query)
            conn.commit()
            return last_user_id
        except Exception as e:
            print(f"Error: {e}")
            return None

    # symbol, name, current_price, change
    def getWatchlist(self):
        """Retrieve watchlist items for the user, including current price, PnL, and change for both stocks and mutual funds."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            # Stock watchlist query
            stock_query = """
                SELECT 
                    e.id AS stock_id,
                    e.symbol AS symbol,
                    e.name AS name,
                    ph.current_price AS current_price,
                    pph.previous_price AS previous_price
                FROM 
                    watchlist w
                JOIN 
                    nasdaq_listed_equities e ON w.stock_id = e.id
                LEFT JOIN 
                    (
                        SELECT 
                            stock_id, 
                            close_price AS current_price 
                        FROM 
                            equity_price_history eph
                        WHERE 
                            eph.price_date = (
                                SELECT MAX(price_date) 
                                FROM equity_price_history 
                                WHERE stock_id = eph.stock_id
                            )
                    ) ph ON w.stock_id = ph.stock_id
                LEFT JOIN 
                    (
                        SELECT 
                            stock_id, 
                            close_price AS previous_price
                        FROM 
                            equity_price_history eph
                        WHERE 
                            eph.price_date = (
                                SELECT MAX(price_date) 
                                FROM equity_price_history 
                                WHERE stock_id = eph.stock_id
                                AND price_date < (
                                    SELECT MAX(price_date)
                                    FROM equity_price_history 
                                    WHERE stock_id = eph.stock_id
                                )
                            )
                    ) pph ON w.stock_id = pph.stock_id
                WHERE 
                    w.user_id = %s;
            """

            cursor.execute(stock_query, (self.user_id,))
            stock_watchlist = cursor.fetchall()

            # Fund watchlist query
            fund_query = """
                SELECT 
                    f.fund_id AS fund_id,
                    f.fund_name AS name,
                    ph.current_price AS current_price,
                    pph.previous_price AS previous_price
                FROM 
                    watchlist w
                JOIN 
                    funds f ON w.fund_id = f.fund_id
                LEFT JOIN 
                    (
                        SELECT 
                            fund_id, 
                            price AS current_price 
                        FROM 
                            fund_price_history fph
                        WHERE 
                            fph.date = (
                                SELECT MAX(date) 
                                FROM fund_price_history 
                                WHERE fund_id = fph.fund_id
                            )
                    ) ph ON w.fund_id = ph.fund_id
                LEFT JOIN 
                    (
                        SELECT 
                            fund_id, 
                            price AS previous_price
                        FROM 
                            fund_price_history fph
                        WHERE 
                            fph.date = (
                                SELECT MAX(date) 
                                FROM fund_price_history 
                                WHERE fund_id = fph.fund_id
                                AND date < (
                                    SELECT MAX(date)
                                    FROM fund_price_history 
                                    WHERE fund_id = fph.fund_id
                                )
                            )
                    ) pph ON w.fund_id = pph.fund_id
                WHERE 
                    w.user_id = %s;
            """

            cursor.execute(fund_query, (self.user_id,))
            fund_watchlist = cursor.fetchall()

            stock_list = []
            for stock in stock_watchlist:
                current_price = stock["current_price"]
                previous_price = stock["previous_price"]
                pnl = None
                change = None

                if current_price is not None and previous_price is not None:
                    pnl = current_price - previous_price
                    change = (pnl / previous_price) * 100 if previous_price != 0 else None
                    pnl = round(pnl, 2)
                    change = round(change, 2) if change is not None else None

                stock_list.append(
                    {
                        "symbol": stock['symbol'],
                        "name": stock['name'],
                        "current_price": current_price,
                        "pnl": pnl,
                        "change": change
                    }
                )

            fund_list = []
            for fund in fund_watchlist:
                current_price = fund["current_price"]
                previous_price = fund["previous_price"]
                pnl = None
                change = None

                if current_price is not None and previous_price is not None:
                    pnl = current_price - previous_price
                    change = (pnl / previous_price) * 100 if previous_price != 0 else None
                    pnl = round(pnl, 2)
                    change = round(change, 2) if change is not None else None

                fund_list.append(
                    {
                        "name": fund['name'],
                        "current_price": current_price,
                        "pnl": pnl,
                        "change": change
                    }
                )
            return stock_list, fund_list

        except Exception as e:
            print(f"Error at getWatchlist(): {e}")
            return None


    def addStockToWatchlist(self, stock_symbol):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT stock_id FROM stock WHERE stock_symbol = %s"
            cursor.execute(query, (stock_symbol,))
            stock = cursor.fetchone()
            if stock:
                stock_id = stock["stock_id"]
                query = "INSERT INTO watchlist (user_id, stock_id) VALUES (%s, %s)"
                cursor.execute(query, (self.user_id, stock_id))
                conn.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error at addStockToWatchlist(): {e}")
            return False
    
    def addFundToWatchlist(self, fund_name):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT fund_id FROM fund WHERE fund_name = %s"
            cursor.execute(query, (fund_name,))
            fund = cursor.fetchone()
            if fund:
                fund_id = fund["fund_id"]
                query = "INSERT INTO watchlist (user_id, fund_id) VALUES (%s, %s)"
                cursor.execute(query, (self.user_id, fund_id))
                conn.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error at addFundToWatchlist(): {e}")
            return False
        
    def register_user_created_by(self,user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO user (first_name, last_name, email, password, role_id, phone_number, dob, street_address, city, state, pincode, country, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.first_name, self.last_name, self.email, self.password, self.role_id, self.phoneno, self.dob, self.street, self.city, self.state, self.pincode, self.country, user_id))
            conn.commit()
            last_user_id = User.get_last_userID()
            return last_user_id
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def getOrders(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM client_orders WHERE client_id = %s"
            cursor.execute(query, (self.user_id,))
            orders = cursor.fetchall()
            return orders
        except Exception as e:
            print(f"Error at getOrders(): {e}")
            return None
        
    def get_all_funds(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    f.fund_id, 
                    f.fund_name, 
                    ph.price AS nav,
                    (SELECT price 
                    FROM fund_price_history 
                    WHERE fund_id = f.fund_id 
                    AND date < (SELECT MAX(date) FROM fund_price_history WHERE fund_id = f.fund_id)
                    ORDER BY date DESC 
                    LIMIT 1) AS previous_price
                FROM 
                    funds f
                LEFT JOIN 
                    (SELECT 
                        fund_id, 
                        price, 
                        date
                    FROM 
                        fund_price_history 
                    WHERE 
                        (fund_id, date) IN 
                        (SELECT fund_id, MAX(date) 
                        FROM fund_price_history 
                        GROUP BY fund_id)) AS ph ON f.fund_id = ph.fund_id
                ORDER BY 
                    f.fund_id;
            """
            cursor.execute(query)
            funds = cursor.fetchall()
            fund_list = []
            for fund in funds:
                fund_id = fund['fund_id']
                fund_name = fund['fund_name']
                nav = fund['nav']
                prev_nav = fund['previous_price']
                percentage_change = None
                if nav is not None and prev_nav is not None:
                    percentage_change = ((nav-prev_nav)/prev_nav)*100
                    percentage_change = round(percentage_change, 2)

                fund_list.append(
                    {
                        "fund_id": fund_id,
                        "fund_name": fund_name,
                        "NAV": nav,
                        "change": percentage_change
                    } 
                )
            
            return fund_list
        except Exception as e:
            print(f"Error at get_all_funds(): {e}")
            return None

    # isko debug krna padega, bohot problems hain by @dang3r
    def getStockHoldings(self):
        """Retrieve stock holdings for the user, including current price, PnL, and change."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            query = """
                SELECT 
                    e.id AS stock_id,
                    e.symbol AS symbol,
                    e.name AS name,
                    p.portfolio_id AS portfolio_id,
                    p.user_id AS user_id,
                    p.quantity AS quantity,
                    p.average_price AS average_price,
                    ph.current_price AS current_price
                FROM 
                    client_portfolio p
                JOIN 
                    nasdaq_listed_equities e ON p.stock_id = e.id
                JOIN 
                    (
                        SELECT 
                            stock_id, 
                            close_price AS current_price
                        FROM 
                            equity_price_history eph
                        WHERE 
                            eph.price_date = (
                                SELECT MAX(price_date) 
                                FROM equity_price_history 
                                WHERE stock_id = eph.stock_id
                            )
                    ) ph ON p.stock_id = ph.stock_id
                WHERE 
                    p.user_id = %s;
            """
            cursor.execute(query, (self.user_id,))
            stocks = cursor.fetchall()
            pnl = None
            change = None
            stock_list = []
            for stock in stocks:
                current_price = stock["current_price"]
                average_price = stock["average_price"]
                if current_price is not None and average_price is not None:
                    pnl = current_price - average_price
                    pnl = round(pnl, 2)
                if pnl is not None and average_price != 0:
                    change = pnl / stock["average_price"]
                    change *= 100
                    change = round(change, 2)
                average_price = round(average_price, 2)

                stock_list.append(
                    {
                        "stock_id": stock['stock_id'],
                        "symbol": stock['symbol'],
                        "name": stock['name'],
                        "portfolio_id": stock['portfolio_id'],
                        "user_id": stock['user_id'],
                        "quantity": stock['quantity'],
                        "average_price": average_price,
                        "current_price": stock['current_price'],
                        "pnl": pnl,
                        "change": change
                    } 
                )
            return stock_list
        except Exception as e:
            print(f"Error at getStockHoldings(): {e}")
            return None

    # isko debug krna padega, bohot problems hain by @dang3r
    def getFundHoldings(self):
        """Retrieve mutual fund holdings for the user, including current price, PnL, and change."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            query = """
            SELECT 
                f.fund_id,
                f.fund_name,
                f.fund_theme,
                p.portfolio_id,
                p.user_id,
                p.quantity,
                p.average_price,
                ph.current_price
            FROM 
                client_portfolio p
            JOIN 
                funds f ON p.fund_id = f.fund_id
            JOIN 
                (
                    SELECT 
                        fund_id, 
                        price AS current_price
                    FROM 
                        fund_price_history fph
                    WHERE 
                        fph.date = (
                            SELECT MAX(date) 
                            FROM fund_price_history 
                            WHERE fund_id = fph.fund_id
                        )
                ) ph ON p.fund_id = ph.fund_id
            WHERE 
                p.user_id = %s;
            """
            cursor.execute(query, (self.user_id,))
            funds = cursor.fetchall()

            fund_list = []
            for fund in funds:
                current_price = fund["current_price"]
                average_price = fund["average_price"]
                pnl = None
                change = None

                if current_price is not None and average_price is not None:
                    pnl = (current_price - average_price) * fund["quantity"]
                    pnl = round(pnl, 2)

                    if average_price != 0:
                        change = (current_price - average_price) / average_price * 100
                        change = round(change, 2)
                average_price = round(average_price, 2)

                fund_list.append(
                    {
                        "fund_id": fund['fund_id'],
                        "fund_name": fund['fund_name'],
                        "fund_theme": fund['fund_theme'],
                        "portfolio_id": fund['portfolio_id'],
                        "user_id": fund['user_id'],
                        "quantity": fund['quantity'],
                        "average_price": average_price,
                        "current_price": fund['current_price'],
                        "pnl": pnl,
                        "change": change
                    }
                )
            return fund_list
        except Exception as e:
            print(f"Error at getFundHoldings(): {e}")
            return None
        
    @staticmethod
    def authenticate(email: str, password: str) -> tuple:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT userID, password, role_id FROM user WHERE email = %s"
            cursor.execute(query, (email))
            user = cursor.fetchall()
            if user is None:
                return None, None
            user = user[0]
            user_id= user['userID']
            hashed_password= user['password']
            role_id= user['role_id']
            if check_password(password=password, hashed_password=hashed_password):
                return user_id, role_id
            else:
                return None, None
        except Exception as e:
            print(f"Error at getOrders(): {e}")
            return None, None
        
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM user"
            cursor.execute(query)
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_current_user():
        user_id = session.get('user_id')
        if user_id:
            d =  User.get_user_by_id(user_id)
            if d:
                return User(
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
    
    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM user WHERE userID = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            if user:
                return user
            else:
                print(f"No user found with user_id: {user_id}")
            return None
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
        
    @staticmethod
    def get_user_darkMode(user_id = None):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = ("SELECT setting_value FROM system_settings WHERE user_id = %s AND setting_name = 'DarkMode'")
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result and result["setting_value"] == '1':
                return 1
            else:
                return 0
        except Exception as e:
            print(f"Error at get_user_darkMode(): {e}")
            return 0

    @staticmethod
    def set_user_darkMode(value:str=None,user_id:int=None):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            value = str(value)
            check_query = ("SELECT setting_value FROM system_settings WHERE user_id = %s AND setting_name = 'DarkMode'")
            cursor.execute(check_query, (user_id,))
            result = cursor.fetchone()
            if result:
                update_query = ("UPDATE system_settings SET setting_value = %s WHERE user_id = %s AND setting_name = 'DarkMode'")
                cursor.execute(update_query, (value, user_id))
            else:
                insert_query = ("INSERT INTO system_settings (setting_name, setting_value, user_id) VALUES ('DarkMode', %s, %s)")
                cursor.execute(insert_query, (value, user_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error at set_user_darkMode(): {e}")
            return False