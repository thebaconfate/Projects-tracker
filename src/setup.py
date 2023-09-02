from pytz import timezone
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
tz = timezone("Europe/Brussels")
bcrypt = Bcrypt()
