# -- Here is the list of all the tables based on the schema you provided:

#     -- user
#     -- roles
#     -- user_roles
#     -- nasdaq_listed_equities
#     -- nasdaq_equity_transactions
#     -- client_portfolio
#     -- funds
#     -- fund_portfolio
#     -- client_orders
#     -- fund_orders
#     -- equity_price_history
#     -- fund_price_history
#     -- watchlist
#     -- user_audit
#     -- system_settings

import pymysql
from datetime import datetime
import os 
from dotenv import load_dotenv

load_dotenv()

timeout = 10
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
  
cur = conn.cursor()

def execute_query(sql_query):
    try:
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        cur.execute(sql_insert_query)
        cur.execute("SET FOREIGN_KEY_CHECKS=1;")
    except Exception as e:
        print(e)
    finally:
        cur.execute("SET FOREIGN_KEY_CHECKS=1;")

sql_insert_query = '''
INSERT INTO roles (role_id, role_name, description_info) VALUES
(1, 'Admin', 'Full access to all system features'),
(2, 'Manager', 'Access to manage user accounts and reports'),
(3, 'Analyst', 'Access to view reports and data'),
(4, 'User', 'Basic access to their own data and features');

'''
execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO user_roles (user_id, role_id) VALUES
(1, 4), -- User
(2, 4), -- User
(3, 4), -- User
(4, 4), -- User
(5, 4), -- User
(6, 4), -- User
(7, 4), -- User
(8, 4), -- User
(9, 4), -- User
(10, 4); -- User
'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO user (first_name, last_name, email, password, role_id, phone_number, dob, street_address, city, state, pincode, country, is_active, created_by, updated_by) VALUES
('John', 'Doe', 'john.doe@example.com', 'hashed_password_1', 3, '9876543210', '1990-05-15', '123 Main St', 'New York', 'NY', '10001', 'USA', TRUE, 1, 1),
('Alice', 'Smith', 'alice.smith@example.com', 'hashed_password_2', 2, '9876543211', '1985-07-21', '456 Elm St', 'Chicago', 'IL', '60601', 'USA', TRUE, 1, 1),
('Bob', 'Johnson', 'bob.johnson@example.com', 'hashed_password_3', 3, '9876543212', '1992-09-10', '789 Maple St', 'San Francisco', 'CA', '94103', 'USA', TRUE, 1, 1),
('Eve', 'Brown', 'eve.brown@example.com', 'hashed_password_4', 4, '9876543213', '1995-11-12', '321 Oak St', 'Los Angeles', 'CA', '90001', 'USA', TRUE, 1, 1),
('Charlie', 'Davis', 'charlie.davis@example.com', 'hashed_password_5', 2, '9876543214', '1987-02-28', '654 Pine St', 'Boston', 'MA', '02108', 'USA', TRUE, 1, 1),
('David', 'Taylor', 'david.taylor@example.com', 'hashed_password_6', 3, '9876543215', '1991-04-22', '987 Cedar St', 'Austin', 'TX', '73301', 'USA', TRUE, 1, 1),
('Grace', 'Williams', 'grace.williams@example.com', 'hashed_password_7', 4, '9876543216', '1989-06-30', '101 Birch St', 'Seattle', 'WA', '98101', 'USA', TRUE, 1, 1),
('Henry', 'Lee', 'henry.lee@example.com', 'hashed_password_8', 3, '9876543217', '1993-08-25', '102 Walnut St', 'Miami', 'FL', '33101', 'USA', TRUE, 1, 1),
('Isabella', 'Garcia', 'isabella.garcia@example.com', 'hashed_password_9', 2, '9876543218', '1994-10-19', '103 Spruce St', 'Houston', 'TX', '77001', 'USA', TRUE, 1, 1),
('Jack', 'Martinez', 'jack.martinez@example.com', 'hashed_password_10', 3, '9876543219', '1988-12-14', '104 Ash St', 'Denver', 'CO', '80201', 'USA', TRUE, 1, 1);
'''
execute_query(sql_insert_query)

sql_insert_query = '''  
INSERT INTO nasdaq_listed_equities (symbol, name, country, sector, industry) VALUES
('AAPL', 'Apple Inc.', 'United States', 'Technology', 'Consumer Electronics'),
('MSFT', 'Microsoft Corp.', 'United States', 'Technology', 'Software'),
('GOOGL', 'Alphabet Inc.', 'United States', 'Communication Services', 'Internet Services'),
('AMZN', 'Amazon.com Inc.', 'United States', 'Consumer Discretionary', 'E-commerce'),
('TSLA', 'Tesla Inc.', 'United States', 'Consumer Discretionary', 'Automobiles'),
('FB', 'Meta Platforms Inc.', 'United States', 'Communication Services', 'Social Media'),
('NFLX', 'Netflix Inc.', 'United States', 'Communication Services', 'Streaming Media'),
('NVDA', 'NVIDIA Corp.', 'United States', 'Technology', 'Semiconductors'),
('INTC', 'Intel Corp.', 'United States', 'Technology', 'Semiconductors'),
('ADBE', 'Adobe Inc.', 'United States', 'Technology', 'Software'),
('CSCO', 'Cisco Systems Inc.', 'United States', 'Technology', 'Networking'),
('ORCL', 'Oracle Corp.', 'United States', 'Technology', 'Software'),
('BA', 'Boeing Co.', 'United States', 'Industrials', 'Aerospace'),
('DIS', 'Walt Disney Co.', 'United States', 'Communication Services', 'Media'),
('XOM', 'Exxon Mobil Corp.', 'United States', 'Energy', 'Oil & Gas'),
('CVX', 'Chevron Corp.', 'United States', 'Energy', 'Oil & Gas'),
('WMT', 'Walmart Inc.', 'United States', 'Consumer Staples', 'Retail'),
('KO', 'Coca-Cola Co.', 'United States', 'Consumer Staples', 'Beverages'),
('PFE', 'Pfizer Inc.', 'United States', 'Healthcare', 'Pharmaceuticals'),
('JNJ', 'Johnson & Johnson', 'United States', 'Healthcare', 'Medical Devices'
);
'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO nasdaq_equity_transactions (user_id, stock_id, transaction_type, quantity, price)
VALUES
(1, 1, 'BUY', 100, 150.00),
(1, 2, 'SELL', 50, 155.00),

(2, 3, 'BUY', 50, 300.00),
(2, 4, 'SELL', 40, 310.00),

(3, 5, 'SELL', 20, 3300.00),
(3, 6, 'BUY', 25, 3200.00),

(4, 7, 'BUY', 10, 2800.00),
(4, 8, 'SELL', 15, 2850.00),

(5, 9, 'SELL', 5, 750.00),
(5, 10, 'BUY', 10, 740.00),

(6, 11, 'BUY', 40, 260.00),
(6, 12, 'SELL', 50, 265.00),

(7, 13, 'BUY', 30, 550.00),
(7, 14, 'SELL', 35, 545.00),

(8, 15, 'SELL', 60, 1000.00),
(8, 16, 'BUY', 65, 990.00),

(9, 17, 'BUY', 70, 110.00),
(9, 18, 'SELL', 80, 115.00),

(10, 19, 'SELL', 80, 60.00),
(10, 20, 'BUY', 90, 65.00);


'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO nasdaq_equity_transactions (user_id, stock_id, transaction_type, quantity, price)
VALUES
(1, 1, 'BUY', 100, 150.00),
(1, 2, 'SELL', 50, 200.00),
(2, 3, 'BUY', 50, 300.00),
(2, 4, 'SELL', 40, 250.00),
(3, 5, 'SELL', 20, 3300.00),
(3, 6, 'BUY', 25, 3400.00),
(4, 7, 'BUY', 10, 2800.00),
(4, 8, 'SELL', 15, 2900.00),
(5, 9, 'SELL', 5, 750.00),
(5, 10, 'BUY', 10, 700.00),
(6, 1, 'BUY', 40, 260.00),
(6, 2, 'SELL', 30, 270.00),
(7, 3, 'BUY', 30, 550.00),
(7, 4, 'SELL', 20, 600.00),
(8, 5, 'SELL', 60, 1000.00),
(8, 6, 'BUY', 40, 1050.00),
(9, 7, 'BUY', 70, 110.00),
(9, 8, 'SELL', 60, 120.00),
(10, 9, 'SELL', 80, 60.00),
(10, 10, 'BUY', 90, 70.00);

'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO client_portfolio (user_id, stock_id, quantity, average_price)
VALUES
(1, 1, 100, 145.00),
(1, 2, 50, 150.00),
(2, 2, 50, 295.00),
(2, 3, 20, 300.00),
(3, 3, 20, 3200.00),
(3, 4, 15, 3300.00),
(4, 4, 10, 2700.00),
(4, 5, 25, 2750.00),
(5, 5, 5, 720.00),
(5, 6, 10, 750.00),
(6, 6, 40, 250.00),
(6, 7, 35, 260.00),
(7, 7, 30, 540.00),
(7, 8, 20, 550.00),
(8, 8, 60, 980.00),
(8, 9, 50, 990.00),
(9, 9, 70, 100.00),
(9, 10, 80, 110.00),
(10, 10, 80, 55.00),
(10, 1, 90, 60.00);

'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO funds (user_id, fund_name, fund_theme, strategy)
VALUES
(1, 'AI Innovation Fund', 'Technology', 'Invest in AI startups and innovation'),
(1, 'Fintech Leaders Fund', 'Finance', 'Focus on leading fintech companies'),
(2, 'Tech Growth Fund', 'Technology', 'Focus on high-growth tech stocks'),
(2, 'Sustainable Future Fund', 'Sustainability', 'Invest in companies with a sustainability focus'),
(3, 'Consumer Discretionary Fund', 'Consumer Products', 'Focus on discretionary consumer spending'),
(3, 'Global Consumer Fund', 'Consumer Products', 'Target global consumer markets'),
(4, 'Industrial Growth Fund', 'Industry', 'Focus on industrial sector growth'),
(4, 'Tech Innovators Fund', 'Technology', 'Invest in innovative technology companies'),
(5, 'Energy Leaders Fund', 'Energy', 'Focus on traditional energy companies'),
(5, 'Clean Energy Fund', 'Energy', 'Invest in clean energy initiatives'),
(6, 'Healthcare Innovation Fund', 'Healthcare', 'Invest in biotech and pharma companies'),
(6, 'Global Healthcare Fund', 'Healthcare', 'Target global healthcare markets'),
(7, 'Green Energy Fund', 'Sustainability', 'Invest in renewable energy companies'),
(7, 'Sustainable Resources Fund', 'Sustainability', 'Invest in sustainable natural resources'),
(8, 'Global Equity Fund', 'Equity', 'Focus on large-cap global companies'),
(8, 'Emerging Markets Fund', 'Emerging Markets', 'Invest in companies from emerging economies'),
(9, 'Global Tech Fund', 'Technology', 'Focus on global tech companies'),
(9, 'Tech Disruptors Fund', 'Technology', 'Invest in companies disrupting the tech space'),
(10, 'Real Estate Investment Fund', 'Real Estate', 'Focus on global real estate markets'),
(10, 'Infrastructure Growth Fund', 'Infrastructure', 'Invest in infrastructure development projects');

'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO fund_portfolio (fund_id, stock_id, quantity, average_price)
VALUES
(1, 1, 200, 145.00),
(1, 2, 150, 300.00),
(2, 5, 150, 730.00),
(2, 6, 120, 750.00),
(3, 3, 100, 3200.00),
(3, 4, 80, 2900.00),
(4, 9, 70, 105.00),
(4, 8, 60, 980.00),
(5, 6, 90, 255.00),
(5, 7, 40, 550.00),
(1, 3, 50, 3200.00),
(1, 4, 60, 2700.00),
(2, 7, 100, 540.00),
(2, 8, 80, 1000.00),
(3, 1, 150, 145.00),
(3, 2, 70, 295.00),
(4, 5, 90, 750.00),
(4, 6, 100, 260.00),
(5, 9, 70, 100.00),
(5, 10, 80, 55.00);

'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO client_orders (client_id, order_date, order_type, symbol, quantity, price, status, created_by, updated_by)
VALUES
(1, '2023-08-01', 'BUY', 'AAPL', 100, 145.50, 'Completed', 1, 1),
(1, '2023-08-12', 'SELL', 'GOOGL', 10, 2800.00, 'Completed', 1, 1),
(1, '2023-08-30', 'SELL', 'JPM', 25, 160.00, 'Pending', 1, 1),

(2, '2023-08-05', 'SELL', 'MSFT', 50, 300.75, 'Pending', 2, 2),
(2, '2023-08-22', 'BUY', 'NVDA', 40, 220.65, 'Pending', 2, 2),

(3, '2023-08-10', 'BUY', 'TSLA', 25, 700.30, 'Completed', 3, 3),
(3, '2023-08-28', 'BUY', 'V', 35, 230.95, 'Completed', 3, 3),

(4, '2023-08-15', 'BUY', 'AMZN', 15, 3500.25, 'Pending', 4, 4),
(4, '2023-09-05', 'SELL', 'NFLX', 20, 600.00, 'Completed', 4, 4),

(5, '2023-08-20', 'SELL', 'NFLX', 30, 600.45, 'Completed', 5, 5),
(5, '2023-09-10', 'BUY', 'DIS', 25, 185.50, 'Pending', 5, 5),

(6, '2023-08-25', 'SELL', 'FB', 20, 320.10, 'Completed', 6, 6),
(6, '2023-09-01', 'BUY', 'BA', 50, 210.75, 'Completed', 6, 6),

(7, '2023-08-05', 'BUY', 'TSLA', 30, 700.00, 'Completed', 7, 7),
(7, '2023-08-30', 'SELL', 'AAPL', 15, 150.00, 'Pending', 7, 7),

(8, '2023-08-15', 'BUY', 'GOOGL', 25, 2750.00, 'Completed', 8, 8),
(8, '2023-09-05', 'SELL', 'MSFT', 20, 310.00, 'Pending', 8, 8),

(9, '2023-08-20', 'BUY', 'AMZN', 10, 3550.00, 'Completed', 9, 9),
(9, '2023-09-10', 'SELL', 'NFLX', 25, 605.00, 'Pending', 9, 9),

(10, '2023-08-25', 'BUY', 'NVDA', 15, 225.00, 'Completed', 10, 10),
(10, '2023-09-15', 'SELL', 'V', 20, 235.00, 'Completed', 10, 10);

'''

execute_query(sql_insert_query)


sql_insert_query = '''
INSERT INTO fund_orders (fund_id, stock_id, quantity, price, order_type, order_date, status, created_by, updated_by) VALUES
(1, 1, 200, 146.50, 'BUY', '2023-07-01', 'Completed', 1, 1),
(1, 2, 50, 2810.00, 'SELL', '2023-07-06', 'Completed', 1, 1),
(1, 3, 75, 165.00, 'SELL', '2023-07-22', 'Pending', 1, 1),

(2, 4, 150, 310.75, 'SELL', '2023-07-02', 'Pending', 2, 2),
(2, 5, 90, 225.65, 'BUY', '2023-07-15', 'Pending', 2, 2),

(3, 6, 100, 710.30, 'BUY', '2023-07-05', 'Completed', 3, 3),
(3, 7, 85, 235.95, 'BUY', '2023-07-20', 'Completed', 3, 3),

(4, 8, 45, 3550.25, 'BUY', '2023-07-10', 'Pending', 4, 4),
(4, 9, 20, 605.00, 'SELL', '2023-07-25', 'Completed', 4, 4),

(5, 10, 80, 610.45, 'SELL', '2023-07-12', 'Completed', 5, 5),
(5, 11, 50, 190.00, 'BUY', '2023-07-28', 'Pending', 5, 5),

(6, 12, 60, 325.10, 'SELL', '2023-07-18', 'Completed', 6, 6),
(6, 13, 100, 215.75, 'BUY', '2023-07-30', 'Completed', 6, 6),

(7, 14, 30, 710.00, 'BUY', '2023-07-05', 'Completed', 7, 7),
(7, 15, 20, 147.00, 'SELL', '2023-07-20', 'Pending', 7, 7),

(8, 16, 50, 2760.00, 'BUY', '2023-07-15', 'Completed', 8, 8),
(8, 17, 25, 315.00, 'SELL', '2023-07-30', 'Pending', 8, 8),

(9, 18, 15, 3570.00, 'BUY', '2023-07-22', 'Completed', 9, 9),
(9, 19, 30, 605.00, 'SELL', '2023-07-30', 'Pending', 9, 9),

(10, 20, 20, 230.00, 'BUY', '2023-07-25', 'Completed', 10, 10),
(10, 1, 30, 240.00, 'SELL', '2023-07-30', 'Completed', 10, 10);

'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO equity_price_history (stock_id, price_date, open_price, close_price, high_price, low_price, volume) VALUES
('1', '2023-09-01', 144.00, 145.50, 146.00, 143.50, 2000000),
('1', '2023-09-02', 145.00, 146.50, 147.00, 144.00, 2100000),

('2', '2023-09-01', 299.00, 300.75, 302.00, 298.50, 1500000),
('2', '2023-09-02', 300.00, 301.50, 303.00, 299.50, 1550000),

('3', '2023-09-01', 695.00, 700.30, 705.00, 690.00, 1200000),
('3', '2023-09-02', 700.00, 705.30, 710.00, 695.00, 1250000),

('4', '2023-09-01', 2780.00, 2800.00, 2820.00, 2760.00, 1000000),
('4', '2023-09-02', 2800.00, 2810.00, 2830.00, 2790.00, 1020000),

('5', '2023-09-01', 3450.00, 3500.25, 3520.00, 3430.00, 900000),
('5', '2023-09-02', 3500.00, 3520.00, 3540.00, 3480.00, 950000);

'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO fund_price_history (fund_id, price, date)
VALUES
(1, 101.25, '2023-08-01'),
(1, 102.50, '2023-08-02'),
(1, 103.75, '2023-08-03'),
(1, 104.00, '2023-08-04'),
(1, 105.25, '2023-08-05'),
(2, 50.75, '2023-08-01'),
(2, 51.50, '2023-08-02'),
(2, 52.25, '2023-08-03'),
(2, 53.00, '2023-08-04'),
(2, 54.25, '2023-08-05'),
(3, 75.00, '2023-08-01'),
(3, 76.25, '2023-08-02'),
(3, 77.50, '2023-08-03'),
(3, 78.00, '2023-08-04'),
(3, 79.25, '2023-08-05'),
(4, 123.45, '2023-08-01'),
(4, 124.00, '2023-08-02'),
(4, 125.75, '2023-08-03'),
(4, 126.50, '2023-08-04'),
(4, 127.25, '2023-08-05'),
(5, 98.30, '2023-08-01'),
(5, 99.00, '2023-08-02'),
(5, 100.50, '2023-08-03'),
(5, 101.20, '2023-08-04'),
(5, 102.00, '2023-08-05');

'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO watchlist (user_id, stock_id, fund_id, added_at)
VALUES
(1, 1, NULL, '2023-08-01 10:00:00'),  -- User 1 watching Stock 1
(1, 2, NULL, '2023-08-02 11:00:00'),  -- User 1 watching Stock 2
(2, 3, NULL, '2023-08-03 12:00:00'),  -- User 2 watching Stock 3
(2, NULL, 1, '2023-08-04 13:00:00'),  -- User 2 watching Fund 1
(3, 4, NULL, '2023-08-05 14:00:00'),  -- User 3 watching Stock 4
(3, NULL, 2, '2023-08-06 15:00:00'),  -- User 3 watching Fund 2
(4, 5, NULL, '2023-08-07 16:00:00'),  -- User 4 watching Stock 5
(4, NULL, 3, '2023-08-08 17:00:00'),  -- User 4 watching Fund 3
(5, 6, NULL, '2023-08-09 18:00:00'),  -- User 5 watching Stock 6
(5, 7, NULL, '2023-08-10 19:00:00'),  -- User 5 watching Stock 7
(6, NULL, 4, '2023-08-11 20:00:00'),  -- User 6 watching Fund 4
(6, NULL, 5, '2023-08-12 21:00:00'),  -- User 6 watching Fund 5
(7, 8, NULL, '2023-08-13 22:00:00'),  -- User 7 watching Stock 8
(7, 9, NULL, '2023-08-14 23:00:00'),  -- User 7 watching Stock 9
(8, NULL, 6, '2023-08-15 08:00:00'),  -- User 8 watching Fund 6
(8, NULL, 7, '2023-08-16 09:00:00'),  -- User 8 watching Fund 7
(9, 10, NULL, '2023-08-17 10:00:00'), -- User 9 watching Stock 10
(9, NULL, 8, '2023-08-18 11:00:00'),  -- User 9 watching Fund 8
(10, NULL, 9, '2023-08-19 12:00:00'), -- User 10 watching Fund 9
(10, NULL, 10, '2023-08-20 13:00:00') -- User 10 watching Fund 10
;
'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO user_audit (user_id, action, field_changed, old_value, new_value, change_date)
VALUES
(1, 'INSERT', NULL, NULL, 'John Doe', '2023-08-01 10:00:00'),  -- User 1 inserted a new record with name 'John Doe'
(2, 'UPDATE', 'email', 'old.email@example.com', 'new.email@example.com', '2023-08-02 11:30:00'),  -- User 2 updated email field
(3, 'DELETE', 'username', 'jane_doe', NULL, '2023-08-03 14:15:00'),  -- User 3 deleted username 'jane_doe'
(4, 'INSERT', NULL, NULL, 'Alice Smith', '2023-08-04 09:45:00'),  -- User 4 inserted a new record with name 'Alice Smith'
(5, 'UPDATE', 'phone', '123-456-7890', '098-765-4321', '2023-08-05 16:00:00'),  -- User 5 updated phone field
(6, 'DELETE', 'address', '123 Elm St', NULL, '2023-08-06 13:30:00'),  -- User 6 deleted address field
(7, 'INSERT', NULL, NULL, 'Bob Johnson', '2023-08-07 08:00:00'),  -- User 7 inserted a new record with name 'Bob Johnson'
(8, 'UPDATE', 'name', 'Michael Brown', 'Mike Brown', '2023-08-08 18:30:00'),  -- User 8 updated name field
(9, 'DELETE', 'email', 'mike.brown@example.com', NULL, '2023-08-09 14:45:00'),  -- User 9 deleted email field
(10, 'INSERT', NULL, NULL, 'Laura White', '2023-08-10 17:00:00'),  -- User 10 inserted a new record with name 'Laura White'
(11, 'UPDATE', 'address', '456 Oak St', '789 Pine St', '2023-08-11 11:15:00'),  -- User 11 updated address field
(12, 'DELETE', 'phone', '555-555-5555', NULL, '2023-08-12 12:30:00'),  -- User 12 deleted phone field
(13, 'INSERT', NULL, NULL, 'Charlie Davis', '2023-08-13 13:45:00'),  -- User 13 inserted a new record with name 'Charlie Davis'
(14, 'UPDATE', 'username', 'charlie_davis', 'charlie_d', '2023-08-14 15:00:00'),  -- User 14 updated username field
(15, 'DELETE', 'name', 'Charlie Davis', NULL, '2023-08-15 10:00:00'),  -- User 15 deleted name field
(16, 'INSERT', NULL, NULL, 'Emily Wilson', '2023-08-16 11:30:00'),  -- User 16 inserted a new record with name 'Emily Wilson'
(17, 'UPDATE', 'email', 'emily.wilson@example.com', 'emily.w@example.com', '2023-08-17 12:15:00'),  -- User 17 updated email field
(18, 'DELETE', 'address', '789 Pine St', NULL, '2023-08-18 09:45:00'),  -- User 18 deleted address field
(19, 'INSERT', NULL, NULL, 'Daniel Lee', '2023-08-19 13:00:00'),  -- User 19 inserted a new record with name 'Daniel Lee'
(20, 'UPDATE', 'phone', '444-444-4444', '555-555-5555', '2023-08-20 14:30:00')  -- User 20 updated phone field
;
'''

execute_query(sql_insert_query)

sql_insert_query = '''
INSERT INTO user_roles (user_id, role_id) VALUES
(1, 4), -- User
(2, 4), -- User
(3, 4), -- User
(4, 4), -- User
(5, 4), -- User
(6, 4), -- User
(7, 4), -- User
(8, 4), -- User
(9, 4), -- User
(10, 4); -- User
'''

execute_query(sql_insert_query)
