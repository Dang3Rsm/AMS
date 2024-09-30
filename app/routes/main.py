from app.models.models import User
from flask import render_template
from flask import Blueprint
from flask import current_app

# @app.route('/')
# def index():
    # return render_template('index.html')

main = Blueprint('main', __name__)


@main.route('/')
def index():
    # print(current_app.config['BRAND_NAME'])
    # User.get_all_users()
    return render_template('index.html',brand_name=current_app.config['BRAND_NAME'])
