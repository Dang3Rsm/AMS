from app.models.models import User
from flask import render_template
from flask import Blueprint
from flask import current_app

# @app.route('/')
# def index():
    # return render_template('index.html')

db = Blueprint('dashboard', __name__)


@db.route('/user')
def user_dashboard():
    user={
        'first_name':"Test"
    }
    return render_template('user_dashboard.html',brand_name=current_app.config['BRAND_NAME'],user=user)