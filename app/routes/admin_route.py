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

@admin.route('/reports', methods=['GET', 'POST'])
@login_required
@role_required(1)
def reports():
    admin = Admin.get_current_user()
    report = admin.get_system_reports()
    return render_template('admin/admin_reports.html', admin_=admin, report=report, brand_name=current_app.config['BRAND_NAME'])

@admin.route('/notifs', methods=['GET', 'POST'])
@login_required
@role_required(1)
def notifs():
    admin = Admin.get_current_user()
    audit_logs = admin.get_audit_logs()
    return render_template('admin/admin_notifs.html', admin_=admin, audit_logs=audit_logs, brand_name=current_app.config['BRAND_NAME'])

@admin.route('/update_dark_mode', methods=['POST'])
@login_required
@role_required(1)
def update_dark_mode():
    admin = Admin.get_current_user()
    user_id = admin.user_id if admin else session.get('user_id')
    if request.is_json:
        data = request.get_json(silent=True) or {}
        val = str(data.get('theme', '0'))
        is_dark = '1' if val in ('1', 'true', True) else '0'
    else:
        theme_val = request.form.getlist('theme')
        is_dark = '1' if ('1' in theme_val or request.form.get('theme') == '1') else '0'

    Admin.set_user_darkMode(value=is_dark, user_id=user_id)
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success', 'darkMode': is_dark})
    return redirect(url_for('admin.settings'))

@admin.route('/update_notifications', methods=['POST'])
@login_required
@role_required(1)
def update_notifications():
    admin = Admin.get_current_user()
    user_id = admin.user_id if admin else session.get('user_id')
    if request.is_json:
        data = request.get_json(silent=True) or {}
        val = str(data.get('notifications', 'disabled')).lower()
        is_enabled = 'enabled' if val in ('enabled', '1', 'true', True) else 'disabled'
    else:
        notif_val = request.form.getlist('notifications')
        is_enabled = 'enabled' if ('enabled' in notif_val or request.form.get('notifications') == 'enabled') else 'disabled'

    Admin.set_user_notifications(value=is_enabled, user_id=user_id)
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success', 'notifications': is_enabled})
    flash('Notification preferences updated.', 'success')
    return redirect(url_for('admin.settings'))

@admin.route('/change_password', methods=['POST'])
@login_required
@role_required(1)
def change_password():
    admin = Admin.get_current_user()
    current_pw = request.form.get('current_password', '')
    new_pw = request.form.get('new_password', '')
    confirm_pw = request.form.get('confirm_password', '')

    from ..security import check_password, generate_hash_password

    if not current_pw or not new_pw or not confirm_pw:
        flash('All password fields are required.', 'danger')
        return redirect(url_for('admin.settings'))

    if not check_password(current_pw, admin.password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('admin.settings'))

    if new_pw != confirm_pw:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('admin.settings'))

    if len(new_pw) < 6:
        flash('Password must be at least 6 characters long.', 'danger')
        return redirect(url_for('admin.settings'))

    hashed = generate_hash_password(new_pw)
    if admin.update_password(hashed):
        flash('Password updated successfully!', 'success')
    else:
        flash('Failed to update password.', 'danger')
    return redirect(url_for('admin.settings'))

@admin.route('/settings', methods=['GET', 'POST'])
@login_required
@role_required(1)
def settings():
    admin = Admin.get_current_user()
    return render_template('admin/admin_settings.html', admin_=admin, brand_name=current_app.config['BRAND_NAME'])

@admin.route('/toggle_activate_user/<int:user_id>', methods=['POST'])
@login_required
@role_required(1)
def toggle_activate_user(user_id):
    admin = Admin.get_current_user()
    admin.toggle_activate_user(user_id)
    flash(f'User status updated.', 'info')
    return redirect(url_for('admin.user_management'))

@admin.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required(1)
def delete_user(user_id):
    admin = Admin.get_current_user()
    if user_id == admin.user_id:
        flash('You cannot delete your own admin account.', 'danger')
        return redirect(url_for('admin.user_management'))
    if admin.delete_user(user_id):
        flash(f'User #{user_id} deleted successfully.', 'success')
    else:
        flash(f'Failed to delete user #{user_id}.', 'danger')
    return redirect(url_for('admin.user_management'))

@admin.route('/edit_user/<int:user_id>', methods=['POST'])
@login_required
@role_required(1)
def edit_user(user_id):
    admin = Admin.get_current_user()
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phoneno = request.form.get('phone_number')
    role_id = request.form.get('role')
    from app.db import get_db_connection
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE user SET first_name=%s, last_name=%s, email=%s, phone_number=%s, role_id=%s, updated_by=%s
                WHERE userID=%s
            """, (first_name, last_name, email, phoneno, role_id, admin.user_id, user_id))
            cursor.execute("""
                INSERT INTO user_audit (user_id, action, field_changed, new_value)
                VALUES (%s, 'UPDATE', 'admin_edit_user', %s)
            """, (admin.user_id, f"Edited user ID {user_id}"))
            conn.commit()
            flash(f'User #{user_id} updated successfully.', 'success')
    except Exception as e:
        flash(f'Failed to update user: {e}', 'danger')
    finally:
        conn.close()
    return redirect(url_for('admin.user_management'))

@admin.route('/add_stock', methods=['POST'])
@login_required
@role_required(1)
def add_stock():
    admin = Admin.get_current_user()
    symbol = request.form.get('symbol', '').strip().upper()
    name = request.form.get('name', '').strip()
    sector = request.form.get('sector', 'Technology').strip()
    industry = request.form.get('industry', 'Software').strip()
    if not symbol or not name:
        flash('Ticker symbol and company name are required.', 'danger')
        return redirect(url_for('admin.stock_management'))
    stock_id = admin.add_stock(symbol=symbol, name=name, sector=sector, industry=industry)
    if stock_id:
        flash(f'Stock {symbol} added successfully!', 'success')
    else:
        flash(f'Failed to add stock {symbol}. It may already exist.', 'danger')
    return redirect(url_for('admin.stock_management'))

@admin.route('/delete_stock/<int:stock_id>', methods=['POST'])
@login_required
@role_required(1)
def delete_stock(stock_id):
    admin = Admin.get_current_user()
    if admin.delete_stock(stock_id):
        flash('Stock deleted successfully.', 'success')
    else:
        flash('Failed to delete stock.', 'danger')
    return redirect(url_for('admin.stock_management'))

@admin.route('/add_fund', methods=['POST'])
@login_required
@role_required(1)
def add_fund():
    admin = Admin.get_current_user()
    fund_name = request.form.get('fund_name', '').strip()
    fund_theme = request.form.get('fund_theme', '').strip()
    strategy = request.form.get('strategy', '').strip()
    try:
        initial_nav = float(request.form.get('initial_nav', 100.0))
    except ValueError:
        initial_nav = 100.0

    if not fund_name:
        flash('Fund name is required.', 'danger')
        return redirect(url_for('admin.fund_management'))

    fund_id = admin.add_fund(fund_name=fund_name, fund_theme=fund_theme, strategy=strategy, initial_nav=initial_nav)
    if fund_id:
        flash(f'Mutual fund "{fund_name}" created successfully!', 'success')
    else:
        flash(f'Failed to create fund "{fund_name}". It may already exist.', 'danger')
    return redirect(url_for('admin.fund_management'))

@admin.route('/delete_fund/<int:fund_id>', methods=['POST'])
@login_required
@role_required(1)
def delete_fund(fund_id):
    admin = Admin.get_current_user()
    if admin.delete_fund(fund_id):
        flash('Mutual fund deleted successfully.', 'success')
    else:
        flash('Failed to delete mutual fund.', 'danger')
    return redirect(url_for('admin.fund_management'))

@admin.route('/add_new_user', methods=['POST'])
@login_required
@role_required(1)
def add_new_user():
    admin = Admin.get_current_user()
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
        first_name=first_name,
        last_name=last_name,
        email=email,
        phoneno=phoneno,
        password=hashed_password,
        role_id=role_id,
        dob=dob,
        street=street,
        city=city,
        state=state,
        pincode=pincode,
        country=country,
        created_by=admin.user_id
    )
    new_user_id = user.register_user_created_by(admin.user_id)
    if new_user_id:
        flash(f'User {first_name} {last_name} created successfully!', 'success')
    else:
        flash('Failed to create user. Email or phone number may already exist.', 'danger')
    return redirect(url_for('admin.user_management'))