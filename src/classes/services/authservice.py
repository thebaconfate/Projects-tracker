from datetime import datetime, timedelta, UTC
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from src.classes.errors.authentication import HashingAlgorithmError, SecretKeyError
from src.classes.models.user import UserDBModel, UserModel


class AuthService:

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.HASHING_ALGORITHM = os.getenv("HASHING_ALGORITHM")
        if self.SECRET_KEY is None:
            raise SecretKeyError()
        if self.HASHING_ALGORITHM is None:
            raise HashingAlgorithmError()

    async def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def hash_password(self, password):
        return self.pwd_context.hash(password)

    async def generate_jwt_token(self, dict, expiration=os.getenv("TOKEN_EXPIRATION")):
        token = dict.copy()
        expires = datetime.now(UTC) + (
            timedelta(minutes=int(expiration))
            if expiration is not None
            else timedelta(minutes=15)
        )
        token.update({"exp": expires})
        return jwt.encode(
            claims=token, key=self.SECRET_KEY, algorithm=self.HASHING_ALGORITHM
        )

    async def authenticate_user(self, user: UserModel, user_in_db: UserDBModel | None):
        if user_in_db is not None and (
            await self.verify_password(user.password, user_in_db.password)
        ):
            user_dict = user_in_db.model_dump()
            del user_dict["password"]
            return user_dict
        else:
            return False
