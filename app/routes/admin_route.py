from app.models.user_model import User
from app.models.admin_model import Admin
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

admin = Blueprint('admin', __name__)

@admin.route('/user_management',methods=['GET', 'POST'])
@login_required
@role_required(1)
def user_management():
    admin = Admin.get_current_user()
    users = admin.get_all_users()
    if not users:
        users = []
    return render_template('admin/admin_user_management.html', admin_=admin, users=users, brand_name=current_app.config['BRAND_NAME'])

@admin.route('/fund_management',methods=['GET', 'POST'])
@login_required
@role_required(1)
def fund_management():
    admin = Admin.get_current_user()
    funds = admin.get_all_funds()
    if not funds:
        funds = []
    return render_template('admin/admin_fund_management.html', admin_=admin, funds=funds, brand_name=current_app.config['BRAND_NAME'])

@admin.route('/stock_management',methods=['GET', 'POST'])
@login_required
@role_required(1)
def stock_management():
    admin = Admin.get_current_user()
    stocks = admin.get_all_stocks()
    if not stocks:
        stocks = []
    return render_template('admin/admin_stock_management.html', admin_=admin, stocks=stocks, brand_name=current_app.config['BRAND_NAME'])

@admin.route('/transactions',methods=['GET', 'POST'])
@login_required
@role_required(1)
def transactions():
    admin = Admin.get_current_user()
    print(f"admin {type(admin)}")
    print(f"admin.user_id {admin.user_id}")
    equity_transactions = admin.get_all_equity_transactions()
    fund_transactions = admin.get_all_fund_transactions()
    if not equity_transactions:
        equity_transactions = []
    if not fund_transactions:
        fund_transactions = []
    return render_template('admin/admin_transactions.html', admin_=admin, transactions={"stocks": equity_transactions, "funds": fund_transactions}, brand_name=current_app.config['BRAND_NAME'])

@admin.route('/reports',methods=['GET', 'POST'])
@login_required
@role_required(1)
def reports():
    admin = Admin.get_current_user()
    return render_template('admin/admin_reports.html', admin_=admin, brand_name=current_app.config['BRAND_NAME'])

@admin.route('/notifs',methods=['GET', 'POST'])
@login_required
@role_required(1)
def notifs():
    admin = Admin.get_current_user()
    return render_template('admin/admin_notifs.html', admin_=admin, brand_name=current_app.config['BRAND_NAME'])


@admin.route('/update_dark_mode', methods=['POST'])
@login_required
@role_required(1)
def update_dark_mode():
    admin = Admin.get_current_user()
    dark_mode = request.form.get('theme','0')
    dark_mode = int(dark_mode)
    if dark_mode:
        dark_mode_value = '1'
    else:
        dark_mode_value = '0'
    user_id = session.get('user_id')
    Admin.set_user_darkMode(value=dark_mode_value, user_id=user_id)
    return redirect(url_for('admin.settings'))

@admin.route('/settings',methods=['GET', 'POST'])
@login_required
@role_required(1)
def settings():
    admin = Admin.get_current_user()
    return render_template('admin/admin_settings.html', admin_=admin, brand_name=current_app.config['BRAND_NAME'])