from fastapi import FastAPI
from db import get_db_connection

# Create tables if they do not exist
def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    user_table = """
    CREATE TABLE IF NOT EXISTS user (
        userID INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        role VARCHAR(50) NOT NULL,
        phone_number VARCHAR(10) UNIQUE NOT NULL,
        dob DATE,
        street_address VARCHAR(255),
        city VARCHAR(50),
        state VARCHAR(50),
        pincode VARCHAR(10),
        country VARCHAR(50),
        is_active BOOLEAN DEFAULT FALSE,
        created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        created_by INT,
        updated_by INT,
        FOREIGN KEY (created_by) REFERENCES user(userID),
        FOREIGN KEY (updated_by) REFERENCES user(userID)
    );
    """

    portfolio_table = """
    CREATE TABLE IF NOT EXISTS portfolio (
        portfolioID INT AUTO_INCREMENT PRIMARY KEY,
        userID INT,
        name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (userID) REFERENCES user(userID)
    );
    """

    asset_table = """
    CREATE TABLE IF NOT EXISTS asset (
        assetID INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        type VARCHAR(50) NOT NULL,
        value DECIMAL(10, 2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    investment_table = """
    CREATE TABLE IF NOT EXISTS investment (
        investmentID INT AUTO_INCREMENT PRIMARY KEY,
        portfolioID INT,
        assetID INT,
        amount DECIMAL(10, 2) NOT NULL,
        investment_date DATE NOT NULL,
        FOREIGN KEY (portfolioID) REFERENCES portfolio(portfolioID),
        FOREIGN KEY (assetID) REFERENCES asset(assetID)
    );
    """

    transaction_table = """
    CREATE TABLE IF NOT EXISTS transaction (
        transactionID INT AUTO_INCREMENT PRIMARY KEY,
        userID INT,
        amount DECIMAL(10, 2) NOT NULL,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        description TEXT,
        FOREIGN KEY (userID) REFERENCES user(userID)
    );
    """

    broker_table = """
    CREATE TABLE IF NOT EXISTS broker (
        brokerID INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        contact_info VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(user_table)
    cursor.execute(portfolio_table)
    cursor.execute(asset_table)
    cursor.execute(investment_table)
    cursor.execute(transaction_table)
    cursor.execute(broker_table)
    connection.commit()
    cursor.close()
