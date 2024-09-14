from flask import Flask, request, jsonify, abort
from flask_mysql import MySQL
from werkzeug.exceptions import HTTPException
from schemas import (
    UserCreate, UserRead,
    PortfolioCreate, PortfolioRead,
    AssetCreate, AssetRead,
    InvestmentCreate, InvestmentRead,
    TransactionCreate, TransactionRead,
    BrokerCreate, BrokerRead
)

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'dbname'
mysql = MySQL(app)

# Utility function for handling database connections
def get_db_connection():
    conn = mysql.get_db()
    return conn.cursor(), conn

# User endpoints
@app.route('/users/', methods=['POST'])
def create_user():
    user = UserCreate(**request.json)
    cursor, conn = get_db_connection()
    add_user = ("INSERT INTO user "
                "(first_name, last_name, email, password, role, phone_number) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
    user_data = (user.first_name, user.last_name, user.email, user.password, user.role, user.phone_number)
    cursor.execute(add_user, user_data)
    conn.commit()
    cursor.execute("SELECT * FROM user WHERE email = %s", (user.email,))
    new_user = cursor.fetchone()
    cursor.close()
    if new_user is None:
        abort(404, description="User not found")
    return jsonify(new_user)

@app.route('/users/', methods=['GET'])
def read_users():
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def read_user(user_id):
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM user WHERE userID = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user is None:
        abort(404, description="User not found")
    return jsonify(user)

# Portfolio endpoints
@app.route('/portfolios/', methods=['POST'])
def create_portfolio():
    portfolio = PortfolioCreate(**request.json)
    cursor, conn = get_db_connection()
    add_portfolio = ("INSERT INTO portfolio "
                     "(userID, name) "
                     "VALUES (%s, %s)")
    portfolio_data = (portfolio.userID, portfolio.name)
    cursor.execute(add_portfolio, portfolio_data)
    conn.commit()
    cursor.execute("SELECT * FROM portfolio WHERE userID = %s AND name = %s", (portfolio.userID, portfolio.name))
    new_portfolio = cursor.fetchone()
    cursor.close()
    if new_portfolio is None:
        abort(404, description="Portfolio not found")
    return jsonify(new_portfolio)

@app.route('/portfolios/', methods=['GET'])
def read_portfolios():
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM portfolio")
    portfolios = cursor.fetchall()
    cursor.close()
    return jsonify(portfolios)

@app.route('/portfolios/<int:portfolio_id>', methods=['GET'])
def read_portfolio(portfolio_id):
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM portfolio WHERE portfolioID = %s", (portfolio_id,))
    portfolio = cursor.fetchone()
    cursor.close()
    if portfolio is None:
        abort(404, description="Portfolio not found")
    return jsonify(portfolio)

# Asset endpoints
@app.route('/assets/', methods=['POST'])
def create_asset():
    asset = AssetCreate(**request.json)
    cursor, conn = get_db_connection()
    add_asset = ("INSERT INTO asset "
                 "(name, type, value) "
                 "VALUES (%s, %s, %s)")
    asset_data = (asset.name, asset.type, asset.value)
    cursor.execute(add_asset, asset_data)
    conn.commit()
    cursor.execute("SELECT * FROM asset WHERE name = %s", (asset.name,))
    new_asset = cursor.fetchone()
    cursor.close()
    if new_asset is None:
        abort(404, description="Asset not found")
    return jsonify(new_asset)

@app.route('/assets/', methods=['GET'])
def read_assets():
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM asset")
    assets = cursor.fetchall()
    cursor.close()
    return jsonify(assets)

@app.route('/assets/<int:asset_id>', methods=['GET'])
def read_asset(asset_id):
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM asset WHERE assetID = %s", (asset_id,))
    asset = cursor.fetchone()
    cursor.close()
    if asset is None:
        abort(404, description="Asset not found")
    return jsonify(asset)

# Investment endpoints
@app.route('/investments/', methods=['POST'])
def create_investment():
    investment = InvestmentCreate(**request.json)
    cursor, conn = get_db_connection()
    add_investment = ("INSERT INTO investment "
                      "(portfolioID, assetID, amount, investment_date) "
                      "VALUES (%s, %s, %s, %s)")
    investment_data = (investment.portfolioID, investment.assetID, investment.amount, investment.investment_date)
    cursor.execute(add_investment, investment_data)
    conn.commit()
    cursor.execute("SELECT * FROM investment WHERE portfolioID = %s AND assetID = %s", (investment.portfolioID, investment.assetID))
    new_investment = cursor.fetchone()
    cursor.close()
    if new_investment is None:
        abort(404, description="Investment not found")
    return jsonify(new_investment)

@app.route('/investments/', methods=['GET'])
def read_investments():
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM investment")
    investments = cursor.fetchall()
    cursor.close()
    return jsonify(investments)

@app.route('/investments/<int:investment_id>', methods=['GET'])
def read_investment(investment_id):
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM investment WHERE investmentID = %s", (investment_id,))
    investment = cursor.fetchone()
    cursor.close()
    if investment is None:
        abort(404, description="Investment not found")
    return jsonify(investment)

# Transaction endpoints
@app.route('/transactions/', methods=['POST'])
def create_transaction():
    transaction = TransactionCreate(**request.json)
    cursor, conn = get_db_connection()
    add_transaction = ("INSERT INTO transaction "
                       "(userID, amount, description) "
                       "VALUES (%s, %s, %s)")
    transaction_data = (transaction.userID, transaction.amount, transaction.description)
    cursor.execute(add_transaction, transaction_data)
    conn.commit()
    cursor.execute("SELECT * FROM transaction WHERE userID = %s AND amount = %s", (transaction.userID, transaction.amount))
    new_transaction = cursor.fetchone()
    cursor.close()
    if new_transaction is None:
        abort(404, description="Transaction not found")
    return jsonify(new_transaction)

@app.route('/transactions/', methods=['GET'])
def read_transactions():
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM transaction")
    transactions = cursor.fetchall()
    cursor.close()
    return jsonify(transactions)

@app.route('/transactions/<int:transaction_id>', methods=['GET'])
def read_transaction(transaction_id):
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM transaction WHERE transactionID = %s", (transaction_id,))
    transaction = cursor.fetchone()
    cursor.close()
    if transaction is None:
        abort(404, description="Transaction not found")
    return jsonify(transaction)

# Broker endpoints
@app.route('/brokers/', methods=['POST'])
def create_broker():
    broker = BrokerCreate(**request.json)
    cursor, conn = get_db_connection()
    add_broker = ("INSERT INTO broker "
                  "(name, contact_info) "
                  "VALUES (%s, %s)")
    broker_data = (broker.name, broker.contact_info)
    cursor.execute(add_broker, broker_data)
    conn.commit()
    cursor.execute("SELECT * FROM broker WHERE name = %s", (broker.name,))
    new_broker = cursor.fetchone()
    cursor.close()
    if new_broker is None:
        abort(404, description="Broker not found")
    return jsonify(new_broker)

@app.route('/brokers/', methods=['GET'])
def read_brokers():
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM broker")
    brokers = cursor.fetchall()
    cursor.close()
    return jsonify(brokers)

@app.route('/brokers/<int:broker_id>', methods=['GET'])
def read_broker(broker_id):
    cursor, _ = get_db_connection()
    cursor.execute("SELECT * FROM broker WHERE brokerID = %s", (broker_id,))
    broker = cursor.fetchone()
    cursor.close()
    if broker is None:
        abort(404, description="Broker not found")
    return jsonify(broker)

# Report endpoint
@app.route('/reports/user/<int:user_id>', methods=['GET'])
def get_user_report(user_id):
    cursor, _ = get_db_connection()
    cursor.execute("""
        SELECT
            u.userID,
            u.first_name,
            u.last_name,
            u.email,
            SUM(t.amount) as total_transactions
        FROM
            user u
            LEFT JOIN transaction t ON u.userID = t.userID
        WHERE
            u.userID = %s
        GROUP BY
            u.userID
    """, (user_id,))
    report = cursor.fetchone()
    cursor.close()
    if report is None:
        abort(404, description="User not found")
    return jsonify(report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
