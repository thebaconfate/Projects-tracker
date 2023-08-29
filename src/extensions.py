
from pytz import timezone
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
tz = timezone('Europe/Brussels')
db = MySQL()
migrate = Migrate()
bcrypt = Bcrypt()