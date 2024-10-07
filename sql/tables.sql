CREATE TABLE IF NOT EXISTS user (
    userID INT AUTO_INCREMENT PRIMARY KEY,              -- Unique identifier for each user
    first_name VARCHAR(50) NOT NULL,                    -- User's first name
    last_name VARCHAR(50) NOT NULL,                     -- User's last name
    email VARCHAR(100) UNIQUE NOT NULL,                 -- User's email address (must be unique)
    password VARCHAR(100) NOT NULL,                     -- Hashed user password
    role_id INT NOT NULL,                               -- Role assigned to the user (admin, fund manager, client, analyst)
    phone_number VARCHAR(10) UNIQUE NOT NULL,           -- User's phone number (must be unique)
    dob DATE,                                           -- User's date of birth
    street_address VARCHAR(255),                        -- User's street address
    city VARCHAR(50),                                   -- City of the user's address
    state VARCHAR(50),                                  -- State of the user's address
    pincode VARCHAR(10),                                -- Postal code of the user's address
    country VARCHAR(50),                                -- Country of the user's address
    is_active BOOLEAN DEFAULT FALSE,                    -- Status of user account (active/inactive)
    created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Timestamp of when the user was created
    updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Timestamp of the last update to the user
    created_by INT,                                     -- ID of the user who created this record
    updated_by INT,                                     -- ID of the user who last updated this record
    FOREIGN KEY (role_id) REFERENCES user_roles(role_id), -- Foreign key linking to the user_roles table to ensure role exists
    FOREIGN KEY (created_by) REFERENCES user(userID),   -- Foreign key linking to the user who created this record
    FOREIGN KEY (updated_by) REFERENCES user(userID)    -- Foreign key linking to the user who last updated this record
);

CREATE TABLE IF NOT EXISTS user_roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,      -- Unique identifier for each role
    role_name VARCHAR(50) UNIQUE NOT NULL,        -- Name of the role (e.g., 'Client', 'Fund Manager'), must be unique and cannot be null
    description_info VARCHAR(255)                -- Description of the role
);

-- Deprecated (useless and changed name)
-- CREATE TABLE IF NOT EXISTS user_roles (
--     user_id INT ,                                -- Unique identifier for each role
--     role_id INT,                                 -- ID of the role assigned to the user
--     PRIMARY KEY (user_id, role_id),              -- Composite primary key to ensure uniqueness
--     FOREIGN KEY (user_id) REFERENCES user(userID),  -- Foreign key linking to the user table
--     FOREIGN KEY (role_id) REFERENCES roles(role_id)  -- Foreign key linking to the roles table
-- );

CREATE TABLE IF NOT EXISTS permission (
    permission_id INT AUTO_INCREMENT PRIMARY KEY,
    permission_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);
CREATE TABLE IF NOT EXISTS role_permission (
    role_id INT,
    permission_id INT,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES user_roles(role_id),
    FOREIGN KEY (permission_id) REFERENCES permission(permission_id)
);

CREATE TABLE IF NOT EXISTS nasdaq_listed_equities (
    id INT AUTO_INCREMENT PRIMARY KEY,                  -- Unique identifier for each stock entry
    symbol VARCHAR(10) NOT NULL,                        -- Stock symbol (e.g., AAPL, MSFT)
    name VARCHAR(100) NOT NULL,                         -- Full name of the stock/company
    country VARCHAR(50) NOT NULL,                       -- Country of the company's registration
    sector VARCHAR(100),                                -- Economic sector of the company (e.g., Technology, Healthcare)
    industry VARCHAR(100),                              -- Specific industry within the sector (e.g., Software, Pharmaceuticals)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Timestamp of when the stock entry was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Timestamp of the last update to the stock entry
    UNIQUE(symbol)                                      -- Ensures each stock symbol is unique
);

CREATE TABLE IF NOT EXISTS nasdaq_equity_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,   -- Unique identifier for each transaction
    user_id INT,                                     -- ID of the user performing the transaction
    stock_id INT,                                    -- ID of the stock involved in the transaction
    transaction_type ENUM('BUY', 'SELL') NOT NULL,            -- Type of transaction: 'BUY' or 'SELL'
    quantity INT NOT NULL,                                    -- Number of shares involved in the transaction
    price DECIMAL(10, 4) NOT NULL,                            -- Price per share at the time of the transaction
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp of when the transaction was made
    FOREIGN KEY (user_id) REFERENCES user(userID),   -- Foreign key linking to the user who made the transaction
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id)  -- Foreign key linking to the stock involved in the transaction
);

CREATE TABLE IF NOT EXISTS fund_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    fund_id INT,
    transaction_type ENUM('BUY', 'SELL') NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,4) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(userID),
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id)
);


CREATE TABLE IF NOT EXISTS client_portfolio (
    portfolio_id INT AUTO_INCREMENT PRIMARY KEY,     -- Unique identifier for each portfolio entry
    user_id INT,                                     -- ID of the user who owns the portfolio
    stock_id INT,                                    -- ID of the stock held in the portfolio
    quantity INT,                                    -- Number of shares of the stock held by the user
    average_price DECIMAL(10, 4),                    -- Average price at which the shares were acquired
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Timestamp of the last update to the portfolio entry
    FOREIGN KEY (user_id) REFERENCES user(userID),   -- Foreign key linking to the user who owns the portfolio
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id)  -- Foreign key linking to the stock held in the portfolio
);

CREATE TABLE IF NOT EXISTS funds (
    fund_id INT AUTO_INCREMENT PRIMARY KEY,        -- Unique identifier for each fund
    user_id INT,                                   -- Foreign key linking to the fund manager in the user table
    fund_name VARCHAR(255) NOT NULL,               -- Name of the fund
    fund_theme VARCHAR(255),                       -- Investment theme of the fund
    strategy VARCHAR(255),                         -- Description of the investment strategy used
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the fund was created
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Timestamp of the last update
    FOREIGN KEY (user_id) REFERENCES user(userID)  -- Foreign key constraint to link fund manager to the user table
);


CREATE TABLE IF NOT EXISTS fund_portfolio (
    portfolio_id INT AUTO_INCREMENT PRIMARY KEY,    -- Unique identifier for each fund manager's portfolio entry
    fund_id INT,                                    -- Foreign key linking to the funds table
    stock_id INT,                                   -- Foreign key linking to the stock/equity table
    quantity INT,                                   -- Quantity of the stock managed by the fund manager
    average_price DECIMAL(10, 4),                   -- Average purchase price of the stock
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Timestamp of the last update
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id),  -- Foreign key constraint to link portfolio to a specific fund
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id)  -- Foreign key constraint for stock reference
);

CREATE TABLE IF NOT EXISTS client_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for each client order
    client_id INT,                                      -- Foreign key linking to the client in the user table
    symbol VARCHAR(10),                                -- Symbol of the stock or equity
    quantity INT,                                      -- Quantity of stock in the order
    price DECIMAL(10, 2),                              -- Price at which the order was executed
    order_type ENUM('BUY', 'SELL') NOT NULL,           -- Indicates whether the order is a buy or sell
    order_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date & time when the order was placed
    status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending', -- Status of the order
    created_by INT,                                   -- ID of the user who created this order
    updated_by INT,                                   -- ID of the user who last updated this order
    FOREIGN KEY (client_id) REFERENCES user(userID),   -- Foreign key constraint to link the client
    -- FOREIGN KEY (symbol) REFERENCES nasdaq_listed_equities(symbol),  -- Foreign key constraint for stock reference
    FOREIGN KEY (created_by) REFERENCES user(userID),   -- Foreign key linking to the user who created the order
    FOREIGN KEY (updated_by) REFERENCES user(userID)    -- Foreign key linking to the user who last updated the order
);

CREATE TABLE IF NOT EXISTS fund_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for each fund order
    fund_id INT,                                        -- Foreign key linking to the fund in the funds table
    stock_id INT,                                       -- Foreign key linking to the stock/equity table
    quantity INT,                                       -- Quantity of stock in the order
    price DECIMAL(10, 4),                               -- Price at which the order was executed
    order_type ENUM('BUY', 'SELL') NOT NULL,            -- Indicates whether the order is a buy or sell
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Timestamp when the order was placed
    status ENUM('Pending', 'Completed', 'Cancelled') NOT NULL, -- Status of the order
    created_by INT,                                     -- ID of the user who created this record
    updated_by INT,                                     -- ID of the user who last updated this record
    FOREIGN KEY (fund_id) REFERENCES fund_portfolio(portfolio_id),  -- Foreign key constraint to link the fund
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id),   -- Foreign key constraint for stock reference
    FOREIGN KEY (created_by) REFERENCES user(userID),    -- Foreign key constraint for the creator
    FOREIGN KEY (updated_by) REFERENCES user(userID)     -- Foreign key constraint for the last updater
);



CREATE TABLE IF NOT EXISTS equity_price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,                -- Unique identifier for each record
    stock_id INT,                                    -- Foreign key to the stock symbol
    price_date DATE,                                -- Date of the price record
    open_price DECIMAL(10, 2),                       -- Opening price of the stock
    close_price DECIMAL(10, 2),                      -- Closing price of the stock
    high_price DECIMAL(10, 2),                       -- Highest price of the stock during the day
    low_price DECIMAL(10, 2),                        -- Lowest price of the stock during the day
    volume BIGINT,                                  -- Volume of shares traded
    percent_change DECIMAL(10, 2),                   -- percent change for day
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the record was created
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id),  -- Foreign key reference to the stock
    UNIQUE(stock_id, price_date)                     -- Ensures there is only one record per stock per date
);


CREATE TABLE IF NOT EXISTS fund_price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for each record
    fund_id INT,                                 -- Foreign key to the fund symbol
    price DECIMAL(10, 2),                        -- Net Asset Value (NAV) or closing price of the fund
    date DATE,                                   -- Date of the record
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp of when the record was created
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id),  -- Assuming there is a `funds` table for mutual funds or ETFs
    UNIQUE(fund_id, date)                       -- Ensures there is only one price record per fund per date
);

CREATE TABLE IF NOT EXISTS watchlist (
    watchlist_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each watchlist entry
    user_id INT,                                -- Foreign key linking to the user who created the watchlist
    stock_id INT,                               -- Foreign key linking to the stock being watched (nullable if watching funds only)
    fund_id INT,                                -- Foreign key linking to the fund being watched (nullable if watching stocks only)
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp indicating when the entry was added to the watchlist
    FOREIGN KEY (user_id) REFERENCES user(userID),  -- Ensures the user exists in the 'user' table
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id),  -- Ensures the stock exists in the 'nasdaq_listed_equities' table
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id)  -- Ensures the fund exists in the 'funds' table (assuming such a table exists)
);

CREATE TABLE IF NOT EXISTS user_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,       -- Unique identifier for each audit record
    user_id INT,                                  -- ID of the user who made the change
    action ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,  -- Type of action performed
    field_changed VARCHAR(100),                   -- Field that was changed (can be NULL for insert actions)
    old_value TEXT,                              -- Previous value of the field (NULL for insert actions)
    new_value TEXT,                              -- New value of the field (NULL for delete actions)
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp of when the change occurred
    FOREIGN KEY (user_id) REFERENCES user(userID)  -- Foreign key to the user table
);


CREATE TABLE IF NOT EXISTS system_settings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    setting_name VARCHAR(255),
    setting_value VARCHAR(255),
    user_id INT
);
