from pytz import timezone
from passlib.context import CryptContext


tz = timezone("Europe/Brussels")
auth = CryptContext(schemes=["bcrypt"], deprecated="auto")
