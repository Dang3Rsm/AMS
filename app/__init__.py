from flask import Flask
from app.config import Config
from app.models.stock_model import Stock
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
app = Flask(__name__)

def create_app():
    app.config.from_object(Config)
    app.secret_key = app.config['SECRET_KEY']

    from app.routes.main_route import main
    from app.routes.auth_route import auth
    from app.routes.dashboard_route import db
    from app.routes.user_route import usr
    from app.routes.admin_route import admin

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(db, url_prefix='/dashboard')
    app.register_blueprint(usr, url_prefix='/dashboard/user')
    app.register_blueprint(admin, url_prefix='/dashboard/admin')

    start_app_scheduler()
    return app

def fetch_stock_data_wrapper():
    with app.app_context():
        Stock.fetch_stock_data()

def start_app_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            func=fetch_stock_data_wrapper,
            trigger="interval",
            seconds=3600,
            id='fetch_stock_data',
            replace_existing=True
        )
        scheduler.start()