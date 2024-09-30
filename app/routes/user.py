from app.models.models import User
from flask import render_template
from flask import Blueprint
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for

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
        return render_template('user_mutualFunds.html',holdings=holdings,brand_name=current_app.config['BRAND_NAME'])
    

@usr.route('/watchlist',methods=['GET', 'POST'])
def watchlist():
    if request.method == 'POST':
        return redirect(url_for('user.watchlist'))
    else:
        return render_template('user_watchlist.html',holdings=holdings,brand_name=current_app.config['BRAND_NAME'])
    
@usr.route('/settings',methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        return redirect(url_for('user.settings'))
    else:
        return render_template('user_settings.html',holdings=holdings,brand_name=current_app.config['BRAND_NAME'])