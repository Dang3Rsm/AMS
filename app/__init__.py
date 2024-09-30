from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Import and register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.dashboard import db
    from app.routes.user import usr

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(db, url_prefix='/dashboard')
    app.register_blueprint(usr, url_prefix='/dashboard/user')

    return app
