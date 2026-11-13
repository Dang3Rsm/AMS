from app.models.user_model import User
from app.models.admin_model import Admin
from flask import render_template, Blueprint, current_app, redirect, url_for
from ..decorators import login_required, role_required

db = Blueprint('dashboard', __name__)

@db.route('/user')
@login_required
def user_dashboard():
    user = User.get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    stocks = user.getStockHoldings() or []
    funds = user.getFundHoldings() or []
    orders = user.getOrders() or []
    total_val = sum(s['current_price'] * s['quantity'] for s in stocks) + sum(f['current_price'] * f['quantity'] for f in funds)
    total_pnl = sum(s['pnl'] for s in stocks) + sum(f['pnl'] for f in funds)
    summary = {
        "portfolio_value": round(total_val, 2),
        "total_pnl": round(total_pnl, 2),
        "holdings_count": len(stocks) + len(funds),
        "orders_count": len(orders)
    }
    return render_template('user/user_dashboard.html', brand_name=current_app.config['BRAND_NAME'], user_=user, summary=summary)

@db.route('/admin')
@login_required
@role_required(1)
def admin_dashboard():
    admin = Admin.get_current_user()
    if not admin:
        return redirect(url_for('auth.login'))
    total_users = admin.count_total_users()
    active_users = admin.count_active_users()
    inactive_users = total_users - active_users
    reports = admin.get_system_reports()
    count = {
        "total": total_users,
        "active": active_users,
        "inactive": inactive_users,
        "equity_volume": reports["equity_volume"],
        "fund_volume": reports["fund_volume"]
    }
    return render_template('admin/admin_dashboard.html', count=count, brand_name=current_app.config['BRAND_NAME'], admin_=admin)