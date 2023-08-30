
from pytz import timezone
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from .classes.database.databaseinterface import DatabaseInterface

login_manager = LoginManager()
tz = timezone('Europe/Brussels')
db = MySQL()
bcrypt = Bcrypt()
dbinterface = DatabaseInterface(db)