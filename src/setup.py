from pytz import timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

tz = timezone("Europe/Brussels")
auth = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
