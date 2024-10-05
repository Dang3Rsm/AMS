from app.models.user_model import User
from flask import Blueprint, render_template
from flask import current_app
from flask import request
from flask import url_for
from flask import redirect
from flask import session
from ..decorators import debug
from ..security import generate_hash_password

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user_id, role_id = User.authenticate(email,password)
        if user_id is None or role_id is None:
           print("ERROR LOGIN: NO USER")
           return redirect('auth.login')
        session['user_id'] = user_id
        session['role_id'] = role_id
        return redirect(url_for('dashboard.user_dashboard'))  
    else:
        return render_template('login.html',brand_name=current_app.config['BRAND_NAME'])
    
@auth.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        session['user_id'] = 18
        session['role_id'] = 4
        return redirect(url_for('dashboard.admin_dashboard'))  
    else:
        return redirect(url_for('dashboard.admin_dashboard'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phoneno = request.form['phone_number']
        dob = request.form['dob']
        street = request.form['street_address']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
        country = request.form['country']
        password = request.form['password']
        role_id = request.form['role']
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
           country= country
           )
        user_id = user.register_user()
        if user_id:
           print("USER CREATED >>> "+ str(user_id))
        else:
           print("FAILED USER CREATION")
        return redirect(url_for('auth.login'))
    else:
        roles = User.get_roles()
        if None == roles:
           roles = []
        return render_template('register.html', brand_name=current_app.config['BRAND_NAME'],roles=roles)
    
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
   session.clear()
   return redirect(url_for('main.index'))