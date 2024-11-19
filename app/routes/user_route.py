from app.models.user_model import User
from app.models.stock_model import Stock
from app.models.fund_model import Fund
from app.routes.main_route import plot_graph
from flask import render_template
from flask import Blueprint
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask import jsonify
from flask import copy_current_request_context
from ..decorators import login_required, role_required
import random
from threading import Thread
import time

usr = Blueprint('user', __name__)

######################### Book Keeping Simlation ##################
def process_order(order_id):
    time.sleep(7)
    with current_app.app_context():
        if random.random() < 0.7:
            complete_order(order_id)
            return True
        else:
            cancel_order(order_id)
            return False

def complete_order(order_id):
    user = User.get_current_user()
    if user.editOrder(order_id=order_id, new_status='Completed'):
        print(f"Order {order_id} completed successfully.")
        return True
    else:
        print(f"Failed to complete order {order_id}.")
        return False

def cancel_order(order_id):
    user = User.get_current_user()
    if user.editOrder(order_id=order_id, new_status='Cancelled'):
        print(f"Order {order_id} cancelled successfully.")
    else:
        print(f"Failed to cancel order {order_id}.")

#####################################################################

@usr.route('/profile',methods=['GET', 'POST'])
@login_required
@role_required(4)
def profile():
    user = User.get_current_user()
    if request.method == 'POST':
        return redirect(url_for('user.profile'))
    else:
        return render_template('user/user_profile.html', user_=user,brand_name=current_app.config['BRAND_NAME'])

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

@usr.route('/place_order', methods=['GET', 'POST'])
@login_required
@role_required(4)
def place_order():
    user = User.get_current_user()
    
    if request.method == 'POST':
        stock_id = request.form.get('stock_id')
        stock_symbol = request.form.get('stock_symbol')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        order_type = request.form.get('transaction_type')
        
        if not stock_id or not quantity or not price or not order_type:
            flash('All fields are required.', 'danger')
            return redirect(url_for('user.place_order'))
        
        try:
            quantity = int(quantity)
            price = float(price)

        except ValueError:
            flash('Quantity and Price must be numeric values.', 'danger')
            return redirect(url_for('user.place_order'))
        
        if quantity <= 0 or price <= 0:
            flash('Quantity and Price must be positive values.', 'danger')
            return redirect(url_for('user.place_order'))
        
        if not stock_id:
            flash(f"Stock with symbol {stock_symbol} not found.", 'danger')
            return redirect(url_for('user.place_order'))

        try:
            order_id =  user.placeOrder(stock_id=stock_id, fund_id=None, order_type=order_type, qty=quantity, price=price)
            if order_id:
                flash('Order placed successfully!', 'success')
                @copy_current_request_context
                def start_processing():
                    process_order(order_id)
                Thread(target=start_processing).start()
                return redirect(url_for('user.current_orders'))
        except Exception as e:
            flash(f"Error placing order: {e}", 'danger')

        return redirect(url_for('user.place_order'))
    
    else:
        stocks_data, _ = user.getWatchlist()
        if not stocks_data:
            stocks_data = []
        
        return render_template('user/user_place_order.html', 
                               user_=user, 
                               watchlist={"stocks": stocks_data}, 
                               brand_name=current_app.config['BRAND_NAME'])


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
        stock_holdings = user.getStockHoldings()
        fund_holdings = user.getFundHoldings()
        if not stock_holdings:
            stock_holdings = []
        if not fund_holdings:
            fund_holdings = []
        return render_template('user/user_holdings.html',user_=user,holdings={"stocks": stock_holdings, "mutualFunds": fund_holdings},brand_name=current_app.config['BRAND_NAME'])
    

@usr.route('/mutual_funds',methods=['GET', 'POST'])
@login_required
@role_required(4)
def funds():
    user = User.get_current_user()
    if request.method == 'POST':
        return redirect(url_for('user.mututal_funds'))
    else:
        mutual_funds = user.get_all_funds()
        fund_holdings = user.getFundHoldings()
        print(fund_holdings)
        
        if not mutual_funds:
            mutual_funds = []
        if not fund_holdings:
            fund_holdings = []
        return render_template('user/user_mutualFunds.html',user_=user,mutual_funds=mutual_funds, fund_holdings=fund_holdings, brand_name=current_app.config['BRAND_NAME'])
    

@usr.route('/watchlist',methods=['GET', 'POST'])
@login_required
@role_required(4)
def watchlist():
    user = User.get_current_user()
    if request.method == 'POST':
        return redirect(url_for('user.watchlist'))
    else:
        stocks_data, funds_data = user.getWatchlist()
        if not stocks_data:
            stocks_data = []
        if not funds_data:
            funds_data = []
        return render_template('user/user_watchlist.html',user_=user,watchlist={"stocks": stocks_data, "funds": funds_data},brand_name=current_app.config['BRAND_NAME'])

@usr.route('/remove_from_watchlist_stock', methods=['POST'])
@login_required
@role_required(4)
def remove_from_watchlist_stock():
    data = request.json
    stock_symbol = data.get('stock_symbol')
    
    if not stock_symbol:
        return jsonify({'status': 'error', 'message': 'Invalid stock symbol.'}), 400

    try:
        user = User.get_current_user()
        user.removeStockFromWatchlist(stock_symbol)
        stocks_list, funds_list = user.getWatchlist()

        watchlist={"stocks": stocks_list, "funds": funds_list}

        return jsonify({'status': 'success', 'message': f'{stock_symbol} removed from watchlist.', 'watchlist': watchlist}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@usr.route('/remove_from_watchlist_fund', methods=['POST'])
@login_required
@role_required(4)
def remove_from_watchlist_fund():
    fund_id = request.json.get('fund_id')
    if not fund_id:
        return jsonify({'status': 'error', 'message': 'Invalid fund ID.'}), 400
    
    # Logic to remove the mutual fund from the user's watchlist
    # Example: delete from the database
    # watchlist.remove_fund(fund_id)
    try:
        user = User.get_current_user()
        user.removeFundFromWatchlist(fund_id)
        stocks_list, funds_list = user.getWatchlist()

        watchlist={"stocks": stocks_list, "funds": funds_list}

        return jsonify({'status': 'success', 'message': f'{fund_id} removed from watchlist.', 'watchlist': watchlist}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@usr.route('/search_stocks', methods=['GET'])
@login_required
@role_required(4)
def search_stocks():
    query = request.args.get('query')
    if query:
        # Fetch stocks from our database
        stocks = Stock.search_stocks(query)  # Implement this in your StockModel
        return jsonify(stocks)  # Return the list of stocks in JSON format
    return jsonify([])  # Return an empty list if no query

@usr.route('/search_funds', methods=['GET'])
@login_required
@role_required(4)
def search_funds():
    query = request.args.get('query')
    if query:
        # Fetch stocks from our database
        funds = Fund.search_funds(query)  # Implement this in your StockModel
        return jsonify(funds)  # Return the list of stocks in JSON format
    return jsonify([])  # Return an empty list if no query

@usr.route('/add_stock_to_watchlist', methods=['POST'])
@login_required
@role_required(4)
def add_stock_to_watchlist():
    data = request.get_json()
    stock_symbol = data.get('stock_symbol')

    if not stock_symbol:
        flash('Please enter a valid stock symbol.', 'danger')
        return jsonify({'status': 'error', 'message': 'Invalid stock symbol'}), 400

    # Logic to add stock to watchlist (find stock by symbol, save to DB)
    # Example:
    # #stock = find_stock_by_symbol(stock_symbol)
    # if stock:
    #     add_to_watchlist(user_id=session['user_id'], stock_id=stock.id)
    #     flash(f'{stock_symbol} added to watchlist!', 'success')
    # else:
    #     flash(f'Stock {stock_symbol} not found.', 'danger')
    
    try:
        stock_symbol = stock_symbol.upper()
        user = User.get_current_user()
        stocks_data, funds_data = user.addStockToWatchlist(stock_symbol)

        watchlist={"stocks": stocks_data, "funds": funds_data}
        return jsonify({'status': 'success', 'watchlist': watchlist}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@usr.route('/add_fund_to_watchlist', methods=['POST'])
@login_required
@role_required(4)
def add_fund_to_watchlist():
    data = request.get_json()
    fund_name = data.get('fund_name')
    # Logic to add fund to watchlist (find fund by name, save to DB)
    # Example:
    # fund = find_fund_by_name(fund_name)
    # if fund:
    #     add_to_watchlist(user_id=session['user_id'], fund_id=fund.id)
    #     flash(f'{fund_name} added to watchlist!', 'success')
    # else:
    #     flash(f'Fund {fund_name} not found.', 'danger')
    if not fund_name:
        flash('Please enter a valid Fund name.', 'danger')
        return jsonify({'status': 'error', 'message': 'Invalid Fund Name'}), 400

    try:
        user = User.get_current_user()
        stocks_data, funds_data = user.addFundToWatchlist(fund_name)

        watchlist={"stocks": stocks_data, "funds": funds_data}
        return jsonify({'status': 'success', 'watchlist': watchlist}), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


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
