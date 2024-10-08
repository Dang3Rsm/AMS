from app.models.user_model import User
from app.models.admin_model import Admin
from app.models.fund_model import Fund
from app.models.stock_model import Stock
from flask import render_template
from flask import Blueprint
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from ..security import generate_hash_password
from ..decorators import login_required, role_required

admin = Blueprint('admin', __name__)

@admin.route('/user_management',methods=['GET', 'POST'])
@login_required
@role_required(1)
def user_management():
    admin = Admin.get_current_user()
    users = admin.get_all_users()
    roles = admin.get_roles()
    if not users:
        users = []
    if not roles:
        roles = []
    return render_template('admin/admin_user_management.html', admin_=admin, users=users, roles=roles, brand_name=current_app.config['BRAND_NAME'])

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

@admin.route('/toggle_activate_user/<int:user_id>',methods=['POST'])
@login_required
@role_required(1)
def toggle_activate_user(user_id):
    admin = Admin.get_current_user()
    admin.toggle_activate_user(user_id)
    return redirect(url_for('admin.user_management'))
    

@admin.route('/add_new_user',methods=['POST'])
@login_required
@role_required(1)
def add_new_user():
    admin = Admin.get_current_user()
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phoneno = request.form.get('phone_number')
        dob = request.form.get('dob')
        street = request.form.get('street_address')
        city = request.form.get('city')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        country = request.form.get('country')
        password = request.form.get('password')
        role_id = request.form.get('role')
        hashed_password = generate_hash_password(password)
        user = User(
           first_name= first_name,
           last_name= last_name,
           email= email,
           phoneno= phoneno,
           password= hashed_password,
           role_id= role_id,
           dob= dob,
           street= street,
           city= city,
           state= state,
           pincode= pincode,
           country= country,
           created_by= admin.user_id
           )
        new_user_id = user.register_user_created_by(admin.user_id)
        if new_user_id:
           print(f"USER CREATED {new_user_id}")
        else:
           print("FAILED USER CREATION")
        return redirect(url_for('admin.user_management'))
    
@admin.route('/add_new_fund', methods=['POST'])
@login_required
@role_required(1)
def add_new_fund():
    admin = Admin.get_current_user()
    if request.method == 'POST':
        fund_name = request.form.get('fundName')
        fund_theme = request.form.get('fundTheme')
        fund_sector = request.form.get('fundSector')
        strategy = request.form.get('strategy')
        
        # Create a new fund instance
        fund = Fund(
            fund_name=fund_name,
            fund_theme=fund_theme,
            fund_sector=fund_sector,
            strategy=strategy,
            Fund_manager=admin.user_id  # Tracking who created the fund
        )
        
        new_fund_id = fund.add_fund()  # Make sure you have this method in your Fund model
        if new_fund_id:
            print(f"FUND CREATED {new_fund_id}")
        else:
            print("FAILED FUND CREATION")
        
        return redirect(url_for('admin.fund_management'))  # Change to the correct route for fund management


@admin.route('/add_new_stock', methods=['POST'])
@login_required
@role_required(1)
def add_new_stock():
    admin = Admin.get_current_user()
    if request.method == 'POST':
        stock_symbol = request.form.get('stocksymbol')
        stock_name = request.form.get('StockName')
        country = request.form.get('stockcountry')
        sector = request.form.get('stocksector')
        industry = request.form.get('stockindustry')
        
        # Create a new stock instance
        stock = Stock(
            symbol=stock_symbol,
            name=stock_name,
            country=country,
            sector=sector,
            industry=industry
        )
        
        new_stock_id = stock.create_stock() 
        if new_stock_id:
            print(f"STOCK CREATED {new_stock_id}")
        else:
            print("FAILED STOCK CREATION")
        
        return redirect(url_for('admin.stock_management')) 

