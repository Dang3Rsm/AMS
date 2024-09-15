from app.models.models import User
from flask import render_template
from flask import Blueprint

# @app.route('/')
# def index():
    # return render_template('index.html')

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
