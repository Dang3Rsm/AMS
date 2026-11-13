from app.db import get_db_connection
from app.models.stock_model import Stock
from flask import session
from ..security import check_password

class User:
    def __init__(self, user_id=None, first_name=None, last_name=None, email=None, phoneno=None, password=None,
                 role_id=None, dob=None, street=None, city=None, state=None, pincode=None, country=None,
                 created_by=None, updated_by=None, is_active=True):
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
        self.darkMode = User.get_user_darkMode(user_id=user_id) if user_id else 0
        self.notifications = User.get_user_notifications(user_id=user_id) if user_id else 'enabled'

    def register_user(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO user (first_name, last_name, email, password, role_id, phone_number, dob, street_address, city, state, pincode, country, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
                """
                cursor.execute(query, (
                    self.first_name, self.last_name, self.email, self.password,
                    self.role_id or 4, self.phoneno, self.dob or None,
                    self.street, self.city, self.state, self.pincode, self.country
                ))
                last_user_id = cursor.lastrowid
                cursor.execute(
                    "UPDATE user SET created_by = %s, updated_by = %s WHERE userID = %s",
                    (last_user_id, last_user_id, last_user_id)
                )
                cursor.execute(
                    "INSERT INTO user_audit (user_id, action, field_changed, new_value) VALUES (%s, %s, %s, %s)",
                    (last_user_id, 'INSERT', 'created_by', str(last_user_id))
                )
                conn.commit()
                return last_user_id
        except Exception as e:
            print(f"Error in register_user: {e}")
            return None
        finally:
            conn.close()

    def register_user_created_by(self, admin_user_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO user (first_name, last_name, email, password, role_id, phone_number, dob, street_address, city, state, pincode, country, is_active, created_by, updated_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, %s, %s)
                """
                cursor.execute(query, (
                    self.first_name, self.last_name, self.email, self.password,
                    self.role_id or 4, self.phoneno, self.dob or None,
                    self.street, self.city, self.state, self.pincode, self.country,
                    admin_user_id, admin_user_id
                ))
                new_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO user_audit (user_id, action, field_changed, new_value) VALUES (%s, 'INSERT', 'admin_create_user', %s)",
                    (admin_user_id, f"Created user ID {new_id}")
                )
                conn.commit()
                return new_id
        except Exception as e:
            print(f"Error in register_user_created_by: {e}")
            return None
        finally:
            conn.close()

    def update_profile(self, first_name, last_name, email, phoneno, dob, street, city, state, pincode, country):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    UPDATE user
                    SET first_name=%s, last_name=%s, email=%s, phone_number=%s, dob=%s,
                        street_address=%s, city=%s, state=%s, pincode=%s, country=%s, updated_by=%s
                    WHERE userID=%s
                """
                cursor.execute(query, (
                    first_name, last_name, email, phoneno, dob or None,
                    street, city, state, pincode, country, self.user_id, self.user_id
                ))
                cursor.execute(
                    "INSERT INTO user_audit (user_id, action, field_changed, new_value) VALUES (%s, 'UPDATE', 'profile', %s)",
                    (self.user_id, email)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False
        finally:
            conn.close()

    def update_password(self, hashed_password):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE user SET password=%s, updated_by=%s WHERE userID=%s", (hashed_password, self.user_id, self.user_id))
                cursor.execute("INSERT INTO user_audit (user_id, action, field_changed, new_value) VALUES (%s, 'UPDATE', 'password', 'changed')", (self.user_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
        finally:
            conn.close()

    def getWatchlist(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                stock_query = """
                    SELECT 
                        e.id AS stock_id,
                        e.symbol AS symbol,
                        e.name AS name,
                        (SELECT close_price FROM equity_price_history WHERE stock_id = e.id ORDER BY price_date DESC LIMIT 1) AS current_price,
                        (SELECT close_price FROM equity_price_history WHERE stock_id = e.id ORDER BY price_date DESC LIMIT 1 OFFSET 1) AS previous_price
                    FROM watchlist w
                    JOIN nasdaq_listed_equities e ON w.stock_id = e.id
                    WHERE w.user_id = %s
                """
                cursor.execute(stock_query, (self.user_id,))
                stock_watchlist = cursor.fetchall()

                fund_query = """
                    SELECT 
                        f.fund_id AS fund_id,
                        f.fund_name AS name,
                        (SELECT price FROM fund_price_history WHERE fund_id = f.fund_id ORDER BY date DESC LIMIT 1) AS current_price,
                        (SELECT price FROM fund_price_history WHERE fund_id = f.fund_id ORDER BY date DESC LIMIT 1 OFFSET 1) AS previous_price
                    FROM watchlist w
                    JOIN funds f ON w.fund_id = f.fund_id
                    WHERE w.user_id = %s
                """
                cursor.execute(fund_query, (self.user_id,))
                fund_watchlist = cursor.fetchall()

                stock_list = []
                for stock in stock_watchlist:
                    curr = float(stock["current_price"]) if stock["current_price"] is not None else 100.0
                    prev = float(stock["previous_price"]) if stock["previous_price"] is not None else curr
                    pnl = round(curr - prev, 2)
                    change = round((pnl / prev) * 100, 2) if prev != 0 else 0.0
                    stock_list.append({
                        "stock_id": stock['stock_id'],
                        "symbol": stock['symbol'],
                        "name": stock['name'],
                        "current_price": round(curr, 2),
                        "pnl": pnl,
                        "change": change
                    })

                fund_list = []
                for fund in fund_watchlist:
                    curr = float(fund["current_price"]) if fund["current_price"] is not None else 100.0
                    prev = float(fund["previous_price"]) if fund["previous_price"] is not None else curr
                    pnl = round(curr - prev, 2)
                    change = round((pnl / prev) * 100, 2) if prev != 0 else 0.0
                    fund_list.append({
                        "fund_id": fund['fund_id'],
                        "name": fund['name'],
                        "current_price": round(curr, 2),
                        "pnl": pnl,
                        "change": change
                    })
                return stock_list, fund_list
        except Exception as e:
            print(f"Error at getWatchlist(): {e}")
            return [], []
        finally:
            conn.close()

    def addStockToWatchlist(self, stock_symbol):
        conn = get_db_connection()
        stock_symbol = stock_symbol.strip().upper()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, symbol FROM nasdaq_listed_equities WHERE UPPER(symbol) = %s", (stock_symbol,))
                stock = cursor.fetchone()
                if not stock:
                    import yfinance as yf
                    comp_name = stock_symbol
                    country = 'United States'
                    sector = 'General'
                    industry = 'General'
                    try:
                        ticker = yf.Ticker(stock_symbol)
                        info = getattr(ticker, 'info', None) or {}
                        if 'shortName' in info or 'longName' in info:
                            comp_name = info.get('shortName') or info.get('longName') or stock_symbol
                            country = info.get('country') or country
                            sector = info.get('sector') or sector
                            industry = info.get('industry') or industry
                    except Exception as e:
                        print(f"yfinance lookup error: {e}")

                    cursor.execute("""
                        INSERT INTO nasdaq_listed_equities (symbol, name, country, sector, industry)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (stock_symbol, comp_name, country, sector, industry))
                    conn.commit()
                    stock_id = cursor.lastrowid
                    stock = {"id": stock_id, "symbol": stock_symbol}
                else:
                    stock_id = stock["id"]

                cursor.execute("SELECT 1 FROM watchlist WHERE user_id = %s AND stock_id = %s", (self.user_id, stock_id))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO watchlist (user_id, stock_id) VALUES (%s, %s)", (self.user_id, stock_id))
                    conn.commit()

                # Check if price history exists; if not, sync from yfinance
                cursor.execute("SELECT 1 FROM equity_price_history WHERE stock_id = %s LIMIT 1", (stock_id,))
                if not cursor.fetchone():
                    Stock.sync_single_stock_price(stock_id, stock["symbol"])

            return self.getWatchlist()
        except Exception as e:
            print(f"Error at addStockToWatchlist(): {e}")
            return None
        finally:
            conn.close()

    def addFundToWatchlist(self, fund_name):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT fund_id FROM funds WHERE LOWER(fund_name) = LOWER(%s)", (fund_name,))
                fund = cursor.fetchone()
                if not fund:
                    return None
                fund_id = fund["fund_id"]
                cursor.execute("SELECT 1 FROM watchlist WHERE user_id = %s AND fund_id = %s", (self.user_id, fund_id))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO watchlist (user_id, fund_id) VALUES (%s, %s)", (self.user_id, fund_id))
                    conn.commit()
            return self.getWatchlist()
        except Exception as e:
            print(f"Error at addFundToWatchlist(): {e}")
            return None
        finally:
            conn.close()

    def removeStockFromWatchlist(self, stock_symbol):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM nasdaq_listed_equities WHERE UPPER(symbol) = UPPER(%s)", (stock_symbol,))
                stock = cursor.fetchone()
                if stock:
                    cursor.execute("DELETE FROM watchlist WHERE user_id = %s AND stock_id = %s", (self.user_id, stock["id"]))
                    conn.commit()
            return self.getWatchlist()
        except Exception as e:
            print(f"Error at removeStockFromWatchlist(): {e}")
            return [], []
        finally:
            conn.close()

    def removeFundFromWatchlist(self, fund_id=None, fund_name=None):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if not fund_id and fund_name:
                    cursor.execute("SELECT fund_id FROM funds WHERE LOWER(fund_name) = LOWER(%s)", (fund_name,))
                    row = cursor.fetchone()
                    fund_id = row['fund_id'] if row else None
                if fund_id:
                    cursor.execute("DELETE FROM watchlist WHERE user_id = %s AND fund_id = %s", (self.user_id, fund_id))
                    conn.commit()
            return self.getWatchlist()
        except Exception as e:
            print(f"Error at removeFundFromWatchlist(): {e}")
            return [], []
        finally:
            conn.close()

    def getOrders(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        COALESCE(e.symbol, f.fund_name, 'ASSET') AS symbol,
                        co.*
                    FROM client_orders co
                    LEFT JOIN nasdaq_listed_equities e ON co.stock_id = e.id
                    LEFT JOIN funds f ON co.fund_id = f.fund_id
                    WHERE co.client_id = %s
                    ORDER BY co.order_datetime DESC
                """
                cursor.execute(query, (self.user_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error at getOrders(): {e}")
            return []
        finally:
            conn.close()

    def placeOrder(self, stock_id, fund_id, order_type, qty, price):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO client_orders (client_id, stock_id, fund_id, quantity, price, order_type, status, created_by, updated_by)
                    VALUES (%s, %s, %s, %s, %s, %s, 'Pending', %s, %s)
                """
                cursor.execute(query, (self.user_id, stock_id, fund_id, qty, price, order_type, self.user_id, self.user_id))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error at placeOrder(): {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def updateOrderStatusById(order_id, new_status):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE client_orders SET status = %s WHERE order_id = %s AND status = 'Pending'", (new_status, order_id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error at updateOrderStatusById(): {e}")
            return False
        finally:
            conn.close()

    def editOrder(self, order_id, new_quantity=None, new_price=None, new_order_type=None, new_status='Pending'):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                updates = []
                parameters = []
                if new_quantity is not None:
                    updates.append("quantity = %s")
                    parameters.append(new_quantity)
                if new_price is not None:
                    updates.append("price = %s")
                    parameters.append(new_price)
                if new_order_type is not None:
                    updates.append("order_type = %s")
                    parameters.append(new_order_type)
                if new_status:
                    updates.append("status = %s")
                    parameters.append(new_status)
                if not updates:
                    return False
                query = f"UPDATE client_orders SET {', '.join(updates)} WHERE order_id = %s"
                parameters.append(order_id)
                cursor.execute(query, tuple(parameters))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error at editOrder(): {e}")
            return False
        finally:
            conn.close()

    def get_all_funds(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        f.fund_id,
                        f.fund_name,
                        f.fund_theme,
                        f.strategy,
                        (SELECT price FROM fund_price_history WHERE fund_id = f.fund_id ORDER BY date DESC LIMIT 1) AS nav,
                        (SELECT price FROM fund_price_history WHERE fund_id = f.fund_id ORDER BY date DESC LIMIT 1 OFFSET 1) AS previous_price
                    FROM funds f
                    ORDER BY f.fund_id
                """
                cursor.execute(query)
                funds = cursor.fetchall()
                fund_list = []
                for fund in funds:
                    nav = float(fund['nav']) if fund['nav'] is not None else 100.0
                    prev_nav = float(fund['previous_price']) if fund['previous_price'] is not None else nav
                    pct = round(((nav - prev_nav) / prev_nav) * 100, 2) if prev_nav != 0 else 0.0
                    fund_list.append({
                        "fund_id": fund['fund_id'],
                        "fund_name": fund['fund_name'],
                        "fund_theme": fund['fund_theme'],
                        "strategy": fund['strategy'],
                        "NAV": round(nav, 2),
                        "change": pct
                    })
                return fund_list
        except Exception as e:
            print(f"Error at get_all_funds(): {e}")
            return []
        finally:
            conn.close()

    def getStockHoldings(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        e.id AS stock_id,
                        e.symbol AS symbol,
                        e.name AS name,
                        p.portfolio_id AS portfolio_id,
                        p.user_id AS user_id,
                        p.quantity AS quantity,
                        p.average_price AS average_price,
                        (SELECT close_price FROM equity_price_history WHERE stock_id = e.id ORDER BY price_date DESC LIMIT 1) AS current_price
                    FROM client_portfolio p
                    JOIN nasdaq_listed_equities e ON p.stock_id = e.id
                    WHERE p.user_id = %s AND p.quantity > 0
                """
                cursor.execute(query, (self.user_id,))
                stocks = cursor.fetchall()
                stock_list = []
                for stock in stocks:
                    avg_p = float(stock["average_price"])
                    curr_p = float(stock["current_price"]) if stock["current_price"] is not None else avg_p
                    qty = int(stock["quantity"])
                    pnl = round((curr_p - avg_p) * qty, 2)
                    change = round(((curr_p - avg_p) / avg_p) * 100, 2) if avg_p != 0 else 0.0
                    stock_list.append({
                        "stock_id": stock['stock_id'],
                        "symbol": stock['symbol'],
                        "name": stock['name'],
                        "portfolio_id": stock['portfolio_id'],
                        "user_id": stock['user_id'],
                        "quantity": qty,
                        "average_price": round(avg_p, 2),
                        "current_price": round(curr_p, 2),
                        "pnl": pnl,
                        "change": change
                    })
                return stock_list
        except Exception as e:
            print(f"Error at getStockHoldings(): {e}")
            return []
        finally:
            conn.close()

    def getFundHoldings(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        f.fund_id,
                        f.fund_name,
                        f.fund_theme,
                        p.portfolio_id,
                        p.user_id,
                        p.quantity,
                        p.average_price,
                        (SELECT price FROM fund_price_history WHERE fund_id = f.fund_id ORDER BY date DESC LIMIT 1) AS current_price
                    FROM client_portfolio p
                    JOIN funds f ON p.fund_id = f.fund_id
                    WHERE p.user_id = %s AND p.quantity > 0
                """
                cursor.execute(query, (self.user_id,))
                funds = cursor.fetchall()
                fund_list = []
                for fund in funds:
                    avg_p = float(fund["average_price"])
                    curr_p = float(fund["current_price"]) if fund["current_price"] is not None else avg_p
                    qty = int(fund["quantity"])
                    pnl = round((curr_p - avg_p) * qty, 2)
                    change = round(((curr_p - avg_p) / avg_p) * 100, 2) if avg_p != 0 else 0.0
                    fund_list.append({
                        "fund_id": fund['fund_id'],
                        "fund_name": fund['fund_name'],
                        "fund_theme": fund['fund_theme'],
                        "portfolio_id": fund['portfolio_id'],
                        "user_id": fund['user_id'],
                        "quantity": qty,
                        "average_price": round(avg_p, 2),
                        "current_price": round(curr_p, 2),
                        "pnl": pnl,
                        "change": change
                    })
                return fund_list
        except Exception as e:
            print(f"Error at getFundHoldings(): {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def authenticate(email: str, password: str) -> tuple:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = "SELECT userID, password, role_id, is_active FROM user WHERE email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                if not user or not user.get('is_active', 1):
                    return None, None
                if check_password(password=password, hashed_password=user['password']):
                    return user['userID'], user['role_id']
                return None, None
        except Exception as e:
            print(f"Error at authenticate(): {e}")
            return None, None
        finally:
            conn.close()

    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM user")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_current_user():
        user_id = session.get('user_id')
        if user_id:
            d = User.get_user_by_id(user_id)
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
        return None

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM user WHERE userID = %s", (user_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_roles():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM user_roles")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_last_userID():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT MAX(userID) AS max_id FROM user")
                row = cursor.fetchone()
                return row["max_id"] if row else None
        except Exception as e:
            print(f"Error at get_last_userID(): {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_user_darkMode(user_id=None):
        if not user_id:
            return 0
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT setting_value FROM system_settings WHERE user_id = %s AND setting_name = 'DarkMode'", (user_id,))
                result = cursor.fetchone()
                return 1 if result and result["setting_value"] == '1' else 0
        except Exception as e:
            print(f"Error at get_user_darkMode(): {e}")
            return 0
        finally:
            conn.close()

    @staticmethod
    def set_user_darkMode(value: str = '0', user_id: int = None):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                value = str(value)
                cursor.execute("SELECT setting_value FROM system_settings WHERE user_id = %s AND setting_name = 'DarkMode'", (user_id,))
                if cursor.fetchone():
                    cursor.execute("UPDATE system_settings SET setting_value = %s WHERE user_id = %s AND setting_name = 'DarkMode'", (value, user_id))
                else:
                    cursor.execute("INSERT INTO system_settings (setting_name, setting_value, user_id) VALUES ('DarkMode', %s, %s)", (value, user_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error at set_user_darkMode(): {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_user_notifications(user_id=None):
        if not user_id:
            return 'enabled'
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT setting_value FROM system_settings WHERE user_id = %s AND setting_name = 'Notifications'", (user_id,))
                result = cursor.fetchone()
                return result["setting_value"] if result else 'enabled'
        except Exception as e:
            print(f"Error at get_user_notifications(): {e}")
            return 'enabled'
        finally:
            conn.close()

    @staticmethod
    def set_user_notifications(value: str = 'enabled', user_id: int = None):
        if not user_id:
            return False
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                value = str(value)
                cursor.execute("SELECT setting_value FROM system_settings WHERE user_id = %s AND setting_name = 'Notifications'", (user_id,))
                if cursor.fetchone():
                    cursor.execute("UPDATE system_settings SET setting_value = %s WHERE user_id = %s AND setting_name = 'Notifications'", (value, user_id))
                else:
                    cursor.execute("INSERT INTO system_settings (setting_name, setting_value, user_id) VALUES ('Notifications', %s, %s)", (value, user_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error at set_user_notifications(): {e}")
            return False
        finally:
            conn.close()