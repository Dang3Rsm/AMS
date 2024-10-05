from app.models.user_model import User
from flask import render_template
from flask import Blueprint
from flask import current_app
from flask import session
from flask import redirect
from flask import url_for
from ..decorators import login_required, role_required, debug


# @app.route('/')
# def index():
    # return render_template('index.html')

db = Blueprint('dashboard', __name__)

@debug
@db.route('/user')
@login_required
@role_required(4)
def user_dashboard():
    user = User.get_current_user()
    if user:
        return render_template('user/user_dashboard.html',brand_name=current_app.config['BRAND_NAME'],user_=user)
    else:
        return redirect(url_for('auth.login'))


@db.route('/admin')
@login_required
@role_required(1)
def admin_dashboard():
    admin = User.get_current_user()
    if admin:
        return render_template('admin/admin_dashboard.html',brand_name=current_app.config['BRAND_NAME'],admin_=admin)
    else:
        return redirect(url_for('auth.login'))