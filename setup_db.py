import os
import pymysql
import bcrypt
from dotenv import load_dotenv

load_dotenv(override=True)

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'ams_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password123')
DB_NAME = os.getenv('DB_NAME', 'AMS_DB')
DB_CHARSET = os.getenv('DB_CHARSET', 'utf8mb4')


def hash_pw(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def init_database():
    conn = pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
        db=DB_NAME, charset=DB_CHARSET, cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0;")

    with open('sql/tables.sql', 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')
        for cmd in sql_commands:
            if cmd.strip():
                cur.execute(cmd)

    cur.execute("DROP TRIGGER IF EXISTS order_completed_trigger;")
    trigger_sql = """
    CREATE TRIGGER order_completed_trigger
    AFTER UPDATE ON client_orders
    FOR EACH ROW
    BEGIN
        IF NEW.status = 'Completed' AND OLD.status != 'Completed' THEN
            IF NEW.stock_id IS NOT NULL THEN
                INSERT INTO nasdaq_equity_transactions (user_id, stock_id, transaction_type, quantity, price)
                VALUES (NEW.client_id, NEW.stock_id, NEW.order_type, NEW.quantity, NEW.price);

                IF NEW.order_type = 'BUY' THEN
                    IF EXISTS (SELECT 1 FROM client_portfolio WHERE user_id = NEW.client_id AND stock_id = NEW.stock_id) THEN
                        UPDATE client_portfolio
                        SET average_price = ((average_price * quantity) + (NEW.price * NEW.quantity)) / (quantity + NEW.quantity),
                            quantity = quantity + NEW.quantity,
                            last_updated = NOW()
                        WHERE user_id = NEW.client_id AND stock_id = NEW.stock_id;
                    ELSE
                        INSERT INTO client_portfolio (user_id, stock_id, quantity, average_price, last_updated)
                        VALUES (NEW.client_id, NEW.stock_id, NEW.quantity, NEW.price, NOW());
                    END IF;
                ELSEIF NEW.order_type = 'SELL' THEN
                    UPDATE client_portfolio
                    SET quantity = GREATEST(0, quantity - NEW.quantity),
                        last_updated = NOW()
                    WHERE user_id = NEW.client_id AND stock_id = NEW.stock_id;

                    DELETE FROM client_portfolio WHERE user_id = NEW.client_id AND stock_id = NEW.stock_id AND quantity <= 0;
                END IF;
            END IF;

            IF NEW.fund_id IS NOT NULL THEN
                INSERT INTO fund_transactions (user_id, fund_id, transaction_type, quantity, price)
                VALUES (NEW.client_id, NEW.fund_id, NEW.order_type, NEW.quantity, NEW.price);

                IF NEW.order_type = 'BUY' THEN
                    IF EXISTS (SELECT 1 FROM client_portfolio WHERE user_id = NEW.client_id AND fund_id = NEW.fund_id) THEN
                        UPDATE client_portfolio
                        SET average_price = ((average_price * quantity) + (NEW.price * NEW.quantity)) / (quantity + NEW.quantity),
                            quantity = quantity + NEW.quantity,
                            last_updated = NOW()
                        WHERE user_id = NEW.client_id AND fund_id = NEW.fund_id;
                    ELSE
                        INSERT INTO client_portfolio (user_id, fund_id, quantity, average_price, last_updated)
                        VALUES (NEW.client_id, NEW.fund_id, NEW.quantity, NEW.price, NOW());
                    END IF;
                ELSEIF NEW.order_type = 'SELL' THEN
                    UPDATE client_portfolio
                    SET quantity = GREATEST(0, quantity - NEW.quantity),
                        last_updated = NOW()
                    WHERE user_id = NEW.client_id AND fund_id = NEW.fund_id;

                    DELETE FROM client_portfolio WHERE user_id = NEW.client_id AND fund_id = NEW.fund_id AND quantity <= 0;
                END IF;
            END IF;
        END IF;
    END
    """
    cur.execute(trigger_sql)

    cur.execute("""
        INSERT IGNORE INTO user_roles (role_id, role_name, description_info) VALUES
        (1, 'Admin', 'Full access to all system features'),
        (2, 'Manager', 'Access to manage user accounts and reports'),
        (3, 'Analyst', 'Access to view reports and data'),
        (4, 'User', 'Client access to trading, portfolio, and mutual funds');
    """)

    cur.execute("""
        INSERT IGNORE INTO permission (permission_id, permission_name, description) VALUES
        (1, 'manage_users', 'Can manage users and their roles'),
        (2, 'execute_trades', 'Can execute trades for clients'),
        (3, 'view_portfolio', 'Can view portfolio details'),
        (4, 'generate_reports', 'Can generate reports');
    """)

    default_pw = hash_pw('password123')
    cur.execute("""
        INSERT INTO user (userID, first_name, last_name, email, password, role_id, phone_number, dob, street_address, city, state, pincode, country, is_active, created_by, updated_by) VALUES
        (1, 'Admin', 'Master', 'admin@ams.com', %s, 1, '9876543210', '1990-05-15', '100 Wall St', 'New York', 'NY', '10005', 'USA', TRUE, 1, 1),
        (2, 'Alice', 'Smith', 'alice@ams.com', %s, 2, '9876543211', '1988-07-21', '456 Elm St', 'Chicago', 'IL', '60601', 'USA', TRUE, 1, 1),
        (3, 'Bob', 'Johnson', 'bob@ams.com', %s, 3, '9876543212', '1992-09-10', '789 Maple St', 'San Francisco', 'CA', '94103', 'USA', TRUE, 1, 1),
        (4, 'Eve', 'Trader', 'user@ams.com', %s, 4, '9876543213', '1995-11-12', '321 Oak St', 'Los Angeles', 'CA', '90001', 'USA', TRUE, 1, 1),
        (5, 'Grace', 'Williams', 'grace@ams.com', %s, 4, '9876543216', '1989-06-30', '101 Birch St', 'Seattle', 'WA', '98101', 'USA', TRUE, 1, 1)
        ON DUPLICATE KEY UPDATE password = VALUES(password), is_active = TRUE;
    """, (default_pw, default_pw, default_pw, default_pw, default_pw))

    cur.execute("""
        INSERT IGNORE INTO nasdaq_listed_equities (id, symbol, name, country, sector, industry) VALUES
        (1, 'AAPL', 'Apple Inc.', 'United States', 'Technology', 'Consumer Electronics'),
        (2, 'MSFT', 'Microsoft Corp.', 'United States', 'Technology', 'Software'),
        (3, 'GOOGL', 'Alphabet Inc.', 'United States', 'Communication Services', 'Internet Services'),
        (4, 'AMZN', 'Amazon.com Inc.', 'United States', 'Consumer Discretionary', 'E-commerce'),
        (5, 'TSLA', 'Tesla Inc.', 'United States', 'Consumer Discretionary', 'Automobiles'),
        (6, 'META', 'Meta Platforms Inc.', 'United States', 'Communication Services', 'Social Media'),
        (7, 'NFLX', 'Netflix Inc.', 'United States', 'Communication Services', 'Streaming Media'),
        (8, 'NVDA', 'NVIDIA Corp.', 'United States', 'Technology', 'Semiconductors'),
        (9, 'INTC', 'Intel Corp.', 'United States', 'Technology', 'Semiconductors'),
        (10, 'ADBE', 'Adobe Inc.', 'United States', 'Technology', 'Software');
    """)

    csv_path = os.path.join(os.path.dirname(__file__), 'sql', 'stock_data_csv', 'nasdaq-listed-symbols.csv')
    if os.path.exists(csv_path):
        import csv
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            stock_rows = []
            for row in reader:
                sym = row.get('Symbol', '').strip()
                name = row.get('Company Name', '').strip()
                if sym and name:
                    stock_rows.append((sym, name, 'United States', 'Technology', 'General'))
            if stock_rows:
                cur.executemany("""
                    INSERT IGNORE INTO nasdaq_listed_equities (symbol, name, country, sector, industry)
                    VALUES (%s, %s, %s, %s, %s)
                """, stock_rows)
        print(f"Loaded {len(stock_rows)} NASDAQ equities from CSV.")

    cur.execute("""
        INSERT IGNORE INTO equity_price_history (stock_id, price_date, open_price, close_price, high_price, low_price, volume, percent_change) VALUES
        (1, '2025-02-10', 225.00, 228.50, 230.00, 224.00, 45000000, 1.55),
        (1, '2025-02-11', 228.50, 232.10, 234.00, 227.50, 48000000, 1.58),
        (2, '2025-02-10', 410.00, 412.00, 415.00, 408.00, 22000000, 0.49),
        (2, '2025-02-11', 412.00, 418.75, 420.00, 411.00, 25000000, 1.64),
        (3, '2025-02-10', 185.00, 186.20, 188.00, 184.00, 30000000, 0.65),
        (3, '2025-02-11', 186.20, 189.40, 191.00, 185.50, 31000000, 1.72),
        (4, '2025-02-10', 205.00, 208.00, 210.00, 204.00, 38000000, 1.46),
        (4, '2025-02-11', 208.00, 212.50, 214.00, 207.00, 40000000, 2.16),
        (5, '2025-02-10', 355.00, 350.00, 360.00, 348.00, 62000000, -1.41),
        (5, '2025-02-11', 350.00, 358.20, 362.00, 349.00, 65000000, 2.34),
        (6, '2025-02-10', 610.00, 615.00, 620.00, 608.00, 15000000, 0.82),
        (6, '2025-02-11', 615.00, 624.50, 628.00, 614.00, 16500000, 1.54),
        (7, '2025-02-10', 880.00, 890.00, 895.00, 875.00, 8000000, 1.14),
        (7, '2025-02-11', 890.00, 902.00, 908.00, 888.00, 8500000, 1.35),
        (8, '2025-02-10', 130.00, 132.50, 135.00, 129.00, 95000000, 1.92),
        (8, '2025-02-11', 132.50, 138.80, 140.00, 132.00, 105000000, 4.75),
        (9, '2025-02-10', 21.00, 20.50, 21.50, 20.20, 42000000, -2.38),
        (9, '2025-02-11', 20.50, 21.10, 21.40, 20.40, 44000000, 2.93),
        (10, '2025-02-10', 450.00, 455.00, 458.00, 448.00, 5000000, 1.11),
        (10, '2025-02-11', 455.00, 462.00, 466.00, 453.00, 5200000, 1.54);
    """)

    cur.execute("""
        INSERT IGNORE INTO funds (fund_id, user_id, fund_name, fund_theme, strategy) VALUES
        (1, 2, 'AI Innovation Fund', 'Technology', 'Invest in high-growth AI & Semiconductor leaders'),
        (2, 2, 'Fintech Leaders Fund', 'Finance', 'Focus on digital payments and modern banking'),
        (3, 2, 'Sustainable Future Fund', 'Sustainability', 'Clean energy and ESG-compliant enterprises'),
        (4, 2, 'Global Healthcare Fund', 'Healthcare', 'Biotech innovators and pharmaceutical giants'),
        (5, 2, 'NASDAQ MegaCap Growth Fund', 'Equity', 'Large-cap US technology compounders');
    """)

    cur.execute("""
        INSERT IGNORE INTO fund_price_history (fund_id, price, date) VALUES
        (1, 112.50, '2025-02-10'), (1, 115.20, '2025-02-11'),
        (2, 64.00, '2025-02-10'),  (2, 65.10, '2025-02-11'),
        (3, 88.40, '2025-02-10'),  (3, 87.90, '2025-02-11'),
        (4, 134.00, '2025-02-10'), (4, 136.40, '2025-02-11'),
        (5, 210.00, '2025-02-10'), (5, 214.80, '2025-02-11');
    """)

    cur.execute("DELETE FROM client_portfolio WHERE user_id = 4;")
    cur.execute("""
        INSERT INTO client_portfolio (user_id, stock_id, fund_id, quantity, average_price) VALUES
        (4, 1, NULL, 25, 210.00),
        (4, 2, NULL, 10, 395.00),
        (4, 8, NULL, 40, 118.50),
        (4, NULL, 1, 15, 104.00),
        (4, NULL, 5, 10, 198.00);
    """)

    cur.execute("DELETE FROM watchlist WHERE user_id = 4;")
    cur.execute("""
        INSERT INTO watchlist (user_id, stock_id, fund_id) VALUES
        (4, 1, NULL), (4, 2, NULL), (4, 5, NULL), (4, 8, NULL),
        (4, NULL, 1), (4, NULL, 3);
    """)

    cur.execute("""
        INSERT IGNORE INTO client_orders (order_id, client_id, stock_id, fund_id, quantity, price, order_type, status, created_by, updated_by) VALUES
        (1, 4, 1, NULL, 25, 210.00, 'BUY', 'Completed', 4, 4),
        (2, 4, 8, NULL, 40, 118.50, 'BUY', 'Completed', 4, 4),
        (3, 4, 5, NULL, 5, 358.20, 'BUY', 'Pending', 4, 4);
    """)

    cur.execute("""
        INSERT IGNORE INTO nasdaq_equity_transactions (transaction_id, user_id, stock_id, transaction_type, quantity, price) VALUES
        (1, 4, 1, 'BUY', 25, 210.00),
        (2, 4, 2, 'BUY', 10, 395.00),
        (3, 4, 8, 'BUY', 40, 118.50);
    """)

    cur.execute("""
        INSERT IGNORE INTO fund_transactions (transaction_id, user_id, fund_id, transaction_type, quantity, price) VALUES
        (1, 4, 1, 'BUY', 15, 104.00),
        (2, 4, 5, 'BUY', 10, 198.00);
    """)

    cur.execute("""
        INSERT IGNORE INTO user_audit (audit_id, user_id, action, field_changed, old_value, new_value) VALUES
        (1, 1, 'INSERT', 'user_created', NULL, 'Admin Master'),
        (2, 4, 'INSERT', 'user_created', NULL, 'Eve Trader');
    """)

    cur.execute("SET FOREIGN_KEY_CHECKS=1;")
    conn.commit()
    cur.close()
    conn.close()
    print("=========================================================")
    print("AMS Database Initialized & Seeded Successfully!")
    print("Admin Login -> Email: admin@ams.com | Password: password123")
    print("User Login  -> Email: user@ams.com  | Password: password123")
    print("=========================================================")


if __name__ == '__main__':
    init_database()
