import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mysqldb import MySQL
from pytz import timezone

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = MySQL()
migrate = Migrate()
bcrypt = Bcrypt()
start_files = None
tz = timezone('Europe/Brussels')



def create_app(testing=True):
    app = Flask(__name__)
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv(
        'MYSQL_DB_TEST') if testing else os.getenv('MYSQL_DB')
    if testing:
        start_files = os.getenv('TEST_FILES')
    else:
        start_files = os.getenv('DEPLOY_FILES')

    login_manager.init_app(app)
    db.init_app(app)
    # migrate.init_app(app, db)
    bcrypt.init_app(app)
    return app
