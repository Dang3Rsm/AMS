from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Import and register blueprints
    from app.routes.main import main
    from app.routes.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
