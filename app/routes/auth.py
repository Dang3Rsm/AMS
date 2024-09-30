from app.models.models import User
from flask import Blueprint, render_template
from flask import current_app
from flask import request
from flask import url_for
from flask import redirect
import bcrypt

auth = Blueprint('auth', __name__)


def generate_hash_password(password):
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(password.encode(), salt)
  return hashed_password.decode()

def check_password(password, hashed_password):
  try:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
  except ValueError as e:
    print("Error checking password:", e)
    return False

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard.user_dashboard'))  
    else:
        return render_template('login.html',brand_name=current_app.config['BRAND_NAME'])

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
        user = User(first_name,last_name,email,phoneno,hashed_password,role_id,dob,street,city,state,pincode,country)
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
   return redirect(url_for('main.index'))