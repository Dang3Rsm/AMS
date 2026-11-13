CREATE TABLE IF NOT EXISTS user_roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description_info VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS permission (
    permission_id INT AUTO_INCREMENT PRIMARY KEY,
    permission_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS role_permission (
    role_id INT,
    permission_id INT,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES user_roles(role_id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permission(permission_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT NOT NULL DEFAULT 4,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    dob DATE,
    street_address VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(50),
    pincode VARCHAR(15),
    country VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT NULL,
    updated_by INT NULL,
    FOREIGN KEY (role_id) REFERENCES user_roles(role_id),
    FOREIGN KEY (created_by) REFERENCES user(userID) ON DELETE SET NULL,
    FOREIGN KEY (updated_by) REFERENCES user(userID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS nasdaq_listed_equities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(15) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    country VARCHAR(50) DEFAULT 'United States',
    sector VARCHAR(100) DEFAULT 'Technology',
    industry VARCHAR(100) DEFAULT 'General',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS funds (
    fund_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    fund_name VARCHAR(255) NOT NULL UNIQUE,
    fund_theme VARCHAR(255),
    strategy VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(userID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS nasdaq_equity_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    stock_id INT,
    transaction_type ENUM('BUY', 'SELL') NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 4) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(userID) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fund_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    fund_id INT,
    transaction_type ENUM('BUY', 'SELL') NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 4) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(userID) ON DELETE CASCADE,
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS client_portfolio (
    portfolio_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stock_id INT DEFAULT NULL,
    fund_id INT DEFAULT NULL,
    quantity INT NOT NULL DEFAULT 0,
    average_price DECIMAL(10, 4) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(userID) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id) ON DELETE CASCADE,
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fund_portfolio (
    portfolio_id INT AUTO_INCREMENT PRIMARY KEY,
    fund_id INT,
    stock_id INT,
    quantity INT,
    average_price DECIMAL(10, 4),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS client_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    stock_id INT DEFAULT NULL,
    fund_id INT DEFAULT NULL,
    quantity INT UNSIGNED NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    order_type ENUM('BUY', 'SELL') NOT NULL,
    order_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending' NOT NULL,
    created_by INT NOT NULL,
    updated_by INT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES user(userID) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id) ON DELETE SET NULL,
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES user(userID) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES user(userID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fund_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    fund_id INT,
    stock_id INT,
    quantity INT,
    price DECIMAL(10, 2),
    order_type ENUM('BUY', 'SELL') NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending' NOT NULL,
    created_by INT,
    updated_by INT,
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES user(userID) ON DELETE SET NULL,
    FOREIGN KEY (updated_by) REFERENCES user(userID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS equity_price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT,
    price_date DATE,
    open_price DECIMAL(10, 2),
    close_price DECIMAL(10, 2),
    high_price DECIMAL(10, 2),
    low_price DECIMAL(10, 2),
    volume BIGINT,
    percent_change DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id) ON DELETE CASCADE,
    UNIQUE(stock_id, price_date)
);

CREATE TABLE IF NOT EXISTS fund_price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fund_id INT,
    price DECIMAL(10, 2),
    date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id) ON DELETE CASCADE,
    UNIQUE(fund_id, date)
);

CREATE TABLE IF NOT EXISTS watchlist (
    watchlist_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    stock_id INT DEFAULT NULL,
    fund_id INT DEFAULT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(userID) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES nasdaq_listed_equities(id) ON DELETE CASCADE,
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    field_changed VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(userID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS system_settings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    setting_name VARCHAR(255),
    setting_value VARCHAR(255),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(userID) ON DELETE CASCADE
);