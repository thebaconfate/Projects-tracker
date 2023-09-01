
from pytz import timezone
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from src.classes.database.databaseinterface import DatabaseInterface

login_manager = LoginManager()
tz = timezone('Europe/Brussels')
bcrypt = Bcrypt()
dbinterface = DatabaseInterface()