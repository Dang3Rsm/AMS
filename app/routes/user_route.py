from app.models.user_model import User
from app.models.stock_model import Stock
from app.models.fund_model import Fund
from flask import (
    render_template, Blueprint, current_app, request,
    redirect, url_for, flash, session, jsonify
)
from ..decorators import login_required
from ..security import generate_hash_password
from threading import Thread
import time

usr = Blueprint('user', __name__)

def process_order_async(app_obj, order_id):
    """Simulates exchange settlement after 4 seconds and triggers portfolio DB update."""
    time.sleep(4)
    with app_obj.app_context():
        User.updateOrderStatusById(order_id, 'Completed')

@usr.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.get_current_user()
    if request.method == 'POST':
        ok = user.update_profile(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email'),
            phoneno=request.form.get('phoneno'),
            dob=request.form.get('dob'),
            street=request.form.get('street'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            pincode=request.form.get('pincode'),
            country=request.form.get('country')
        )
        if ok:
            flash('Profile updated successfully!', 'success')
        else:
            flash('Error updating profile.', 'danger')
        return redirect(url_for('user.profile'))
    return render_template('user/user_profile.html', user_=user, brand_name=current_app.config['BRAND_NAME'])

@usr.route('/current_orders', methods=['GET', 'POST'])
@login_required
def current_orders():
    user = User.get_current_user()
    orders = user.getOrders() or []
    return render_template('user/user_current_orders.html', user_=user, orders=orders, brand_name=current_app.config['BRAND_NAME'])

@usr.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    user = User.get_current_user()
    if request.method == 'POST':
        stock_id = request.form.get('stock_id')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        order_type = request.form.get('transaction_type')

        if not stock_id or not quantity or not price or not order_type:
            flash('Please select a stock from your watchlist and enter a valid quantity.', 'danger')
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

        if order_type == 'SELL':
            holdings = user.getStockHoldings() or []
            owned_qty = sum(h['quantity'] for h in holdings if h['stock_id'] == int(stock_id))
            if owned_qty < quantity:
                flash(f'Cannot sell {quantity} shares. You currently own {owned_qty} shares.', 'danger')
                return redirect(url_for('user.place_order'))

        order_id = user.placeOrder(stock_id=int(stock_id), fund_id=None, order_type=order_type, qty=quantity, price=price)
        if order_id:
            flash('Order placed! Executing trade on exchange (completes in ~4s)...', 'success')
            app_obj = current_app._get_current_object()
            Thread(target=process_order_async, args=(app_obj, order_id), daemon=True).start()
            return redirect(url_for('user.current_orders'))
        else:
            flash('Failed to place order.', 'danger')
            return redirect(url_for('user.place_order'))
    else:
        stocks_data, _ = user.getWatchlist()
        return render_template(
            'user/user_place_order.html',
            user_=user,
            watchlist={"stocks": stocks_data or []},
            brand_name=current_app.config['BRAND_NAME']
        )

@usr.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    user = User.get_current_user()
    if User.updateOrderStatusById(order_id, 'Cancelled'):
        flash(f'Order #{order_id} cancelled.', 'info')
    else:
        flash(f'Order #{order_id} is already settled and cannot be modified.', 'warning')
    return redirect(url_for("user.current_orders"))

@usr.route('/holdings', methods=['GET', 'POST'])
@login_required
def holdings():
    user = User.get_current_user()
    stock_holdings = user.getStockHoldings() or []
    fund_holdings = user.getFundHoldings() or []
    return render_template(
        'user/user_holdings.html',
        user_=user,
        holdings={"stocks": stock_holdings, "mutualFunds": fund_holdings},
        brand_name=current_app.config['BRAND_NAME']
    )

@usr.route('/mutual_funds', methods=['GET', 'POST'])
@login_required
def funds():
    user = User.get_current_user()
    if request.method == 'POST':
        fund_id = request.form.get('fund_id')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        order_type = request.form.get('transaction_type', 'BUY')
        try:
            qty = int(quantity)
            nav = float(price)
            if qty <= 0:
                flash('Quantity must be greater than zero.', 'danger')
                return redirect(url_for('user.funds'))

            if order_type == 'SELL':
                fund_holdings = user.getFundHoldings() or []
                owned_units = sum(f['quantity'] for f in fund_holdings if f['fund_id'] == int(fund_id))
                if owned_units < qty:
                    flash(f'Cannot sell {qty} units. You currently hold {owned_units} units.', 'danger')
                    return redirect(url_for('user.funds'))

            order_id = user.placeOrder(stock_id=None, fund_id=int(fund_id), order_type=order_type, qty=qty, price=nav)
            if order_id:
                flash(f'Mutual fund {order_type} order placed! Settling...', 'success')
                app_obj = current_app._get_current_object()
                Thread(target=process_order_async, args=(app_obj, order_id), daemon=True).start()
                return redirect(url_for('user.current_orders'))
        except Exception as e:
            flash(f'Error placing mutual fund order: {e}', 'danger')
        return redirect(url_for('user.funds'))
    else:
        mutual_funds = user.get_all_funds() or []
        fund_holdings = user.getFundHoldings() or []
        _, watched_funds = user.getWatchlist()
        watched_names = [f['name'] for f in (watched_funds or [])]
        return render_template(
            'user/user_mutualFunds.html',
            user_=user,
            mutual_funds=mutual_funds,
            fund_holdings=fund_holdings,
            watched_names=watched_names,
            brand_name=current_app.config['BRAND_NAME']
        )

@usr.route('/watchlist', methods=['GET', 'POST'])
@login_required
def watchlist():
    user = User.get_current_user()
    stocks_data, funds_data = user.getWatchlist()
    return render_template(
        'user/user_watchlist.html',
        user_=user,
        watchlist={"stocks": stocks_data or [], "funds": funds_data or []},
        brand_name=current_app.config['BRAND_NAME']
    )

@usr.route('/remove_from_watchlist_stock', methods=['POST'])
@login_required
def remove_from_watchlist_stock():
    data = request.get_json(silent=True) or {}
    stock_symbol = data.get('stock_symbol')
    if not stock_symbol:
        return jsonify({'status': 'error', 'message': 'Invalid stock symbol.'}), 400
    user = User.get_current_user()
    stocks_list, funds_list = user.removeStockFromWatchlist(stock_symbol)
    return jsonify({
        'status': 'success',
        'message': f'{stock_symbol} removed from watchlist.',
        'watchlist': {"stocks": stocks_list, "funds": funds_list}
    }), 200

@usr.route('/remove_from_watchlist_fund', methods=['POST'])
@login_required
def remove_from_watchlist_fund():
    data = request.get_json(silent=True) or {}
    fund_id = data.get('fund_id')
    fund_name = data.get('fund_name')
    if not fund_id and not fund_name:
        return jsonify({'status': 'error', 'message': 'Invalid fund identifier.'}), 400
    user = User.get_current_user()
    stocks_list, funds_list = user.removeFundFromWatchlist(fund_id=fund_id, fund_name=fund_name)
    return jsonify({
        'status': 'success',
        'message': 'Removed from watchlist.',
        'watchlist': {"stocks": stocks_list, "funds": funds_list}
    }), 200

@usr.route('/search_stocks', methods=['GET'])
@login_required
def search_stocks():
    query = request.args.get('query', '').strip()
    if query:
        return jsonify(Stock.search_stocks(query))
    return jsonify([])

@usr.route('/search_funds', methods=['GET'])
@login_required
def search_funds():
    query = request.args.get('query', '').strip()
    if query:
        return jsonify(Fund.search_funds(query))
    return jsonify([])

@usr.route('/add_stock_to_watchlist', methods=['POST'])
@login_required
def add_stock_to_watchlist():
    data = request.get_json(silent=True) or {}
    stock_symbol = data.get('stock_symbol', '').strip().upper()
    if not stock_symbol:
        return jsonify({'status': 'error', 'message': 'Invalid stock symbol'}), 400
    user = User.get_current_user()
    result = user.addStockToWatchlist(stock_symbol)
    if result is None:
        return jsonify({'status': 'error', 'message': f'Ticker {stock_symbol} could not be added or found on Yahoo Finance.'}), 404
    stocks_data, funds_data = result
    return jsonify({'status': 'success', 'watchlist': {"stocks": stocks_data, "funds": funds_data}}), 200

@usr.route('/add_fund_to_watchlist', methods=['POST'])
@login_required
def add_fund_to_watchlist():
    data = request.get_json(silent=True) or {}
    fund_name = data.get('fund_name', '').strip()
    if not fund_name:
        return jsonify({'status': 'error', 'message': 'Invalid Fund Name'}), 400
    user = User.get_current_user()
    result = user.addFundToWatchlist(fund_name)
    if result is None:
        return jsonify({'status': 'error', 'message': f'Fund "{fund_name}" not found.'}), 404
    stocks_data, funds_data = result
    return jsonify({'status': 'success', 'watchlist': {"stocks": stocks_data, "funds": funds_data}}), 200

@usr.route('/update_dark_mode', methods=['POST'])
@login_required
def update_dark_mode():
    user = User.get_current_user()
    user_id = user.user_id if user else session.get('user_id')
    if request.is_json:
        data = request.get_json(silent=True) or {}
        val = str(data.get('theme', '0'))
        is_dark = '1' if val in ('1', 'true', True) else '0'
    else:
        theme_val = request.form.getlist('theme')
        is_dark = '1' if ('1' in theme_val or request.form.get('theme') == '1') else '0'

    User.set_user_darkMode(value=is_dark, user_id=user_id)
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success', 'darkMode': is_dark})
    return redirect(url_for('user.settings'))

@usr.route('/update_notifications', methods=['POST'])
@login_required
def update_notifications():
    user = User.get_current_user()
    user_id = user.user_id if user else session.get('user_id')
    if request.is_json:
        data = request.get_json(silent=True) or {}
        val = str(data.get('notifications', 'disabled')).lower()
        is_enabled = 'enabled' if val in ('enabled', '1', 'true', True) else 'disabled'
    else:
        notif_val = request.form.getlist('notifications')
        is_enabled = 'enabled' if ('enabled' in notif_val or request.form.get('notifications') == 'enabled') else 'disabled'

    User.set_user_notifications(value=is_enabled, user_id=user_id)
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success', 'notifications': is_enabled})
    flash('Notification preferences updated.', 'success')
    return redirect(url_for('user.settings'))

@usr.route('/change_password', methods=['POST'])
@login_required
def change_password():
    user = User.get_current_user()
    current_pw = request.form.get('current_password', '')
    new_pw = request.form.get('new_password', '')
    confirm_pw = request.form.get('confirm_password', '')

    from ..security import check_password, generate_hash_password

    if not current_pw or not new_pw or not confirm_pw:
        flash('All password fields are required.', 'danger')
        return redirect(url_for('user.settings'))

    if not check_password(current_pw, user.password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('user.settings'))

    if new_pw != confirm_pw:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('user.settings'))

    if len(new_pw) < 6:
        flash('Password must be at least 6 characters long.', 'danger')
        return redirect(url_for('user.settings'))

    hashed = generate_hash_password(new_pw)
    if user.update_password(hashed):
        flash('Password changed successfully!', 'success')
    else:
        flash('Failed to change password.', 'danger')
    return redirect(url_for('user.settings'))

@usr.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = User.get_current_user()
    return render_template('user/user_settings.html', user_=user, brand_name=current_app.config['BRAND_NAME'])