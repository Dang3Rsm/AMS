from app.models.user_model import User
from flask import render_template
from flask import Blueprint
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from ..decorators import login_required, role_required

# @app.route('/')
# def index():
    # return render_template('index.html')

usr = Blueprint('user', __name__)



@usr.route('/current_orders',methods=['GET', 'POST'])
@login_required
@role_required(4)
def current_orders():
    user = User.get_current_user()
    if request.method == 'POST':
        pass
    else:
        orders = user.getOrders()
        if not orders:
            orders = []
        return render_template('user/user_current_orders.html', user_=user, orders=orders, brand_name=current_app.config['BRAND_NAME'])

@usr.route('/place_order',methods=['GET', 'POST'])
@login_required
@role_required(4)
def place_order():
    user = User.get_current_user()
    if request.method == 'POST':
        return redirect(url_for('user.place_order'))
    else:
        exchanges = {"NSE","BSE","MCX"}
        return render_template('user/user_place_order.html',user_=user,exchanges=exchanges,brand_name=current_app.config['BRAND_NAME'])

@usr.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
@role_required(4)
def edit_order(order_id):
    print(f'envoked edit order with order_id: ({order_id})')    
    return redirect(url_for("user.current_orders"))

@usr.route('/holdings',methods=['GET', 'POST'])
@login_required
@role_required(4)
def holdings():
    user = User.get_current_user()
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
        return render_template('user/user_holdings.html',user_=user,holdings=holdings,brand_name=current_app.config['BRAND_NAME'])
    

@usr.route('/mutual_funds',methods=['GET', 'POST'])
@login_required
@role_required(4)
def funds():
    user = User.get_current_user()
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
        return render_template('user/user_mutualFunds.html',user_=user,mutual_funds=mutual_funds,brand_name=current_app.config['BRAND_NAME'])
    

@usr.route('/watchlist',methods=['GET', 'POST'])
@login_required
@role_required(4)
def watchlist():
    user = User.get_current_user()
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
        return render_template('user/user_watchlist.html',user_=user,watchlist={"stocks": stocks_data, "funds": funds_data},brand_name=current_app.config['BRAND_NAME'])

@usr.route('/remove_from_watchlist/stock/<string:stock_symbol>', methods=['POST'])
@login_required
@role_required(4)
def remove_from_watchlist_stock(stock_symbol):
    # Logic to remove the stock from the user's watchlist
    # Example: delete from the database
    # watchlist.remove_stock(stock_symbol)

    flash(f'Stock {stock_symbol} removed from your watchlist.', 'success')
    return redirect(url_for('watchlist'))

@usr.route('/remove_from_watchlist/fund/<int:fund_id>', methods=['POST'])
@login_required
@role_required(4)
def remove_from_watchlist_fund(fund_id):
    # Logic to remove the mutual fund from the user's watchlist
    # Example: delete from the database
    # watchlist.remove_fund(fund_id)

    flash(f'Fund with ID {fund_id} removed from your watchlist.', 'success')
    return redirect(url_for('watchlist'))


@usr.route('/add_stock_to_watchlist', methods=['POST'])
@login_required
@role_required(4)
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
@login_required
@role_required(4)
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


@usr.route('/update_dark_mode', methods=['POST'])
@login_required
@role_required(4)
def update_dark_mode():
    dark_mode = request.form.get('theme','0')
    dark_mode = int(dark_mode)
    if dark_mode:
        dark_mode_value = '1'
    else:
        dark_mode_value = '0'
    user_id = session.get('user_id')
    User.set_user_darkMode(value=dark_mode_value, user_id=user_id)
    return redirect(url_for('user.settings'))



@usr.route('/settings', methods=['GET', 'POST'])
@login_required
@role_required(4)
def settings():
    user = User.get_current_user()
    if request.method == 'POST':
    #     name = request.form['name']
    #     email = request.form['email']
    #     dob = request.form['dob']
    #     password = request.form['password']
    #     confirm_password = request.form['confirm_password']
        # update_user_settings(user.id, name, email, dob, theme, notifications)
        # Perform update logic (e.g., update database)
        # Validate password change, if necessary
        # darkMode = int(darkMode)
        # User.set_user_darkMode(darkMode,user.user_id)

        # # flash('Settings updated successfully!', 'success')
        # print(f"SET DARKMODE: {darkMode}")
        return redirect(url_for('user.settings'))

    # Render settings page with current user settings
    # user = get_current_user()  # Replace with logic to get current user's data
    return render_template('user/user_settings.html', user_=user,brand_name=current_app.config['BRAND_NAME'])
