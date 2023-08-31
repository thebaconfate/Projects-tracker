"""Workhours project."""
__version__ = "0.1.0"
import os
from .routes import bp
from dotenv import load_dotenv
from flask import Flask
from .setup import login_manager, bcrypt

login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
start_files = None


def create_app(testing=True):
    app = Flask(__name__)
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY')
    if testing:
        start_files = os.getenv('TEST_FILES')
    else:
        start_files = os.getenv('DEPLOY_FILES')

    login_manager.init_app(app)
    # migrate.init_app(app, db)
    bcrypt.init_app(app)
    app.register_blueprint(bp)
    return app
