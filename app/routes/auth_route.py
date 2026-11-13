from app.models.user_model import User
from flask import Blueprint, render_template, current_app, request, url_for, redirect, session, flash
from ..security import generate_hash_password

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user_id, role_id = User.authenticate(email, password)

        if user_id is None or role_id is None:
            flash("Invalid email/password or account deactivated.", "danger")
            return redirect(url_for('auth.login'))

        session['user_id'] = user_id
        session['role_id'] = role_id

        if role_id == 1:
            return redirect(url_for('dashboard.admin_dashboard'))
        else:
            return redirect(url_for('dashboard.user_dashboard'))
    return render_template('login.html', brand_name=current_app.config['BRAND_NAME'])

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('auth.register'))

        hashed_password = generate_hash_password(password)
        user = User(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email'),
            phoneno=request.form.get('phone_number'),
            password=hashed_password,
            role_id=int(request.form.get('role', 4)),
            dob=request.form.get('dob') or None,
            street=request.form.get('street_address'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            pincode=request.form.get('pincode'),
            country=request.form.get('country')
        )
        user_id = user.register_user()
        if user_id:
            flash("Account created! Please log in.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Registration failed. Email or phone number may already be in use.", "danger")
            return redirect(url_for('auth.register'))
    else:
        roles = User.get_roles() or []
        return render_template('register.html', brand_name=current_app.config['BRAND_NAME'], roles=roles)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('main.index'))