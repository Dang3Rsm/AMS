from app.models.user_model import User
from flask import render_template
from flask import Blueprint
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
# @app.route('/')
# def index():
    # return render_template('index.html')

usr = Blueprint('user', __name__)

@usr.route('/current_orders',methods=['GET', 'POST'])
def current_orders():
    if request.method == 'POST':
        pass
    else:
        orders = [
            {
                "createTime": "2024-09-30 10:45:32",
                "exchangeSegment": "NSE",
                "tradingSymbol": "RELIANCE",
                "validity": "DAY",
                "quantity": 100,
                "price": 2400.50,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-30 11:00:15",
                "exchangeSegment": "BSE",
                "tradingSymbol": "TCS",
                "validity": "DAY",
                "quantity": 50,
                "price": 3650.00,
                "orderStatus": "Pending"
            },
            {
                "createTime": "2024-09-29 14:22:10",
                "exchangeSegment": "NSE",
                "tradingSymbol": "INFY",
                "validity": "IOC",
                "quantity": 75,
                "price": 1500.75,
                "orderStatus": "Cancelled"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            },
            {
                "createTime": "2024-09-28 09:35:50",
                "exchangeSegment": "NSE",
                "tradingSymbol": "HDFC",
                "validity": "GTC",
                "quantity": 200,
                "price": 2950.00,
                "orderStatus": "Completed"
            }
        ]
        return render_template('user_current_orders.html', orders=orders, brand_name=current_app.config['BRAND_NAME'])

@usr.route('/place_order',methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        return redirect(url_for('user.place_order'))
    else:
        exchanges = {"NSE","BSE","MCX"}
        return render_template('user_place_order.html',exchanges=exchanges,brand_name=current_app.config['BRAND_NAME'])
    

@usr.route('/holdings',methods=['GET', 'POST'])
def holdings():
    if request.method == 'POST':
        return redirect(url_for('user.holdings'))
    else:
        holdings = [
                {
                    "exchange": "NSE",
                    "tradingSymbol": "RELIANCE",
                    "totalQty": 50,
                    "avgCostPrice": 2000.00
                },
                {
                    "exchange": "NSE",
                    "tradingSymbol": "TCS",
                    "totalQty": 30,
                    "avgCostPrice": 3500.50
                },
                {
                    "exchange": "BSE",
                    "tradingSymbol": "INFY",
                    "totalQty": 25,
                    "avgCostPrice": 1500.75
                },
                {
                    "exchange": "NSE",
                    "tradingSymbol": "HDFC",
                    "totalQty": 40,
                    "avgCostPrice": 2900.00
                },
                {
                    "exchange": "NSE",
                    "tradingSymbol": "HCLTECH",
                    "totalQty": 35,
                    "avgCostPrice": 800.00
                },
                {
                    "exchange": "BSE",
                    "tradingSymbol": "WIPRO",
                    "totalQty": 60,
                    "avgCostPrice": 650.25
                },
                {
                    "exchange": "NSE",
                    "tradingSymbol": "AXISBANK",
                    "totalQty": 20,
                    "avgCostPrice": 850.50
                },
                {
                    "exchange": "BSE",
                    "tradingSymbol": "ICICIBANK",
                    "totalQty": 15,
                    "avgCostPrice": 780.00
                },
                {
                    "exchange": "NSE",
                    "tradingSymbol": "TATAMOTORS",
                    "totalQty": 45,
                    "avgCostPrice": 500.75
                },
                {
                    "exchange": "BSE",
                    "tradingSymbol": "MARUTI",
                    "totalQty": 10,
                    "avgCostPrice": 7200.00
                }
            ]
        return render_template('user_holdings.html',holdings=holdings,brand_name=current_app.config['BRAND_NAME'])
    

@usr.route('/mutual_funds',methods=['GET', 'POST'])
def funds():
    if request.method == 'POST':
        return redirect(url_for('user.mututal_funds'))
    else:
        mutual_funds = [
            {"id": 1, "name": "Vanguard 500 Index Fund", "current_price": 315.75, "change": 0.9},
            {"id": 2, "name": "Fidelity Contrafund", "current_price": 225.50, "change": -1.2},
            {"id": 3, "name": "T. Rowe Price Blue Chip Growth Fund", "current_price": 139.60, "change": 1.4},
            {"id": 4, "name": "American Funds Growth Fund", "current_price": 156.80, "change": 0.2},
            {"id": 5, "name": "Dodge & Cox Stock Fund", "current_price": 204.15, "change": -0.5},
            {"id": 6, "name": "TIAA-CREF Social Choice Fund", "current_price": 126.95, "change": 0.7}
        ]
        return render_template('user_mutualFunds.html',mutual_funds=mutual_funds,brand_name=current_app.config['BRAND_NAME'])
    

@usr.route('/watchlist',methods=['GET', 'POST'])
def watchlist():
    if request.method == 'POST':
        return redirect(url_for('user.watchlist'))
    else:
        stocks_data = [
            {"symbol": "AAPL", "company_name": "Apple Inc.", "current_price": 145.09, "change": 1.5},
            {"symbol": "TSLA", "company_name": "Tesla Inc.", "current_price": 700.12, "change": -0.8},
            {"symbol": "AMZN", "company_name": "Amazon.com Inc.", "current_price": 3342.88, "change": 0.9},
            {"symbol": "GOOGL", "company_name": "Alphabet Inc.", "current_price": 2800.22, "change": 1.2},
            {"symbol": "MSFT", "company_name": "Microsoft Corporation", "current_price": 299.87, "change": 2.3},
            {"symbol": "NFLX", "company_name": "Netflix Inc.", "current_price": 589.00, "change": -1.7},
            {"symbol": "FB", "company_name": "Meta Platforms Inc.", "current_price": 351.64, "change": 0.5},
            {"symbol": "NVDA", "company_name": "NVIDIA Corporation", "current_price": 195.80, "change": 3.1},
            {"symbol": "DIS", "company_name": "The Walt Disney Company", "current_price": 177.12, "change": -0.3},
            {"symbol": "BABA", "company_name": "Alibaba Group Holding Ltd.", "current_price": 210.50, "change": -1.0},
            {"symbol": "AMD", "company_name": "Advanced Micro Devices, Inc.", "current_price": 120.56, "change": 1.7},
            {"symbol": "SPOT", "company_name": "Spotify Technology S.A.", "current_price": 248.92, "change": -0.4}
        ]


        funds_data = [
            {"fund_id": 1, "fund_name": "Vanguard 500 Index Fund", "nav": 350.45, "change": 0.4},
            {"fund_id": 2, "fund_name": "Fidelity Contrafund", "nav": 104.23, "change": -0.2}
        ]
        return render_template('watchlist.html',watchlist={"stocks": stocks_data, "funds": funds_data},brand_name=current_app.config['BRAND_NAME'])

@usr.route('/remove_from_watchlist/stock/<string:stock_symbol>', methods=['POST'])
def remove_from_watchlist_stock(stock_symbol):
    # Logic to remove the stock from the user's watchlist
    # Example: delete from the database
    # watchlist.remove_stock(stock_symbol)

    flash(f'Stock {stock_symbol} removed from your watchlist.', 'success')
    return redirect(url_for('watchlist'))

@usr.route('/remove_from_watchlist/fund/<int:fund_id>', methods=['POST'])
def remove_from_watchlist_fund(fund_id):
    # Logic to remove the mutual fund from the user's watchlist
    # Example: delete from the database
    # watchlist.remove_fund(fund_id)

    flash(f'Fund with ID {fund_id} removed from your watchlist.', 'success')
    return redirect(url_for('watchlist'))


@usr.route('/add_stock_to_watchlist', methods=['POST'])
def add_stock_to_watchlist():
    stock_symbol = request.form.get('stock_symbol')
    # Logic to add stock to watchlist (find stock by symbol, save to DB)
    # Example:
    # #stock = find_stock_by_symbol(stock_symbol)
    # if stock:
    #     add_to_watchlist(user_id=session['user_id'], stock_id=stock.id)
    #     flash(f'{stock_symbol} added to watchlist!', 'success')
    # else:
    #     flash(f'Stock {stock_symbol} not found.', 'danger')
    return redirect(url_for('user.watchlist'))

@usr.route('/add_fund_to_watchlist', methods=['POST'])
def add_fund_to_watchlist():
    fund_name = request.form.get('fund_name')
    # Logic to add fund to watchlist (find fund by name, save to DB)
    # Example:
    # fund = find_fund_by_name(fund_name)
    # if fund:
    #     add_to_watchlist(user_id=session['user_id'], fund_id=fund.id)
    #     flash(f'{fund_name} added to watchlist!', 'success')
    # else:
    #     flash(f'Fund {fund_name} not found.', 'danger')
    return redirect(url_for('user.watchlist'))

    
@usr.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Handle form submission and update user settings
        user_id = 69
        name = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        theme = request.form['theme']
        notifications = request.form['notifications']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Perform update logic (e.g., update database)
        # Validate password change, if necessary

        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings'))

    # Render settings page with current user settings
    # user = get_current_user()  # Replace with logic to get current user's data
    user = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'dob': '1990-05-15',
        'theme': 'dark',
        'notifications': 'enabled'
    }
    return render_template('user_settings.html', user=user, brand_name=current_app.config['BRAND_NAME'])
