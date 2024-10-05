from app.models.user_model import User
from flask import render_template
from flask import Blueprint
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
# @app.route('/')
# def index():
    # return render_template('index.html')

admin = Blueprint('admin', __name__)

@admin.route('/user',methods=['GET', 'POST'])
def users_list():
    pass