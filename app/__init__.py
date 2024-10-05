from flask import Flask
from app.config import Config
import secrets
from app.models.stock_model import Stock
from apscheduler.schedulers.background import BackgroundScheduler

# Create a scheduler instance globally so it can be accessed in the function
scheduler = BackgroundScheduler()
app = Flask(__name__)

def create_app():

    # Load configuration
    app.config.from_object(Config)
    app.secret_key = secrets.token_hex(16)

    # Import and register blueprints
    from app.routes.main_route import main
    from app.routes.auth_route import auth
    from app.routes.dashboard_route import db
    from app.routes.user_route import usr

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(db, url_prefix='/dashboard')
    app.register_blueprint(usr, url_prefix='/dashboard/user')

    # Initialize the scheduler
    start_app_scheduler(app)

    return app

def fetch_stock_data_wrapper():
    # Use the application context to run the stock data fetch function
    with app.app_context():
        Stock.fetch_stock_data()

def start_app_scheduler(app):
    # Add the job to the scheduler
    # scheduler.add_job(func=fetch_stock_data_wrapper, trigger="interval", seconds=10, id='fetch_stock_data', replace_existing=True)
    scheduler.add_job(func=fetch_stock_data_wrapper, trigger="cron", hour=0, minute=52, id='fetch_stock_data', replace_existing=True)
    # Start the scheduler
    scheduler.start()
