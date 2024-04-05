from datetime import datetime, timedelta, UTC
import os
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from src.classes.database.interface import DatabaseInterface
from src.classes.errors.authentication import (
    HashingAlgorithmError,
    IncorrectPasswordError,
    SecretKeyError,
    UserNotFoundError,
)
from src.classes.models.user import DBUserModel, LoginUserModel
from src.classes.models.auth import Token

TOKEN_EXPIRATION = int(os.getenv("TOKEN_EXPIRATION"))
SECRET_KEY = os.getenv("SECRET_KEY")
HASHING_ALGORITHM = os.getenv("HASHING_ALGORITHM")


class AuthService:
    def __init__(self):
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.SECRET_KEY = SECRET_KEY
        self.HASHING_ALGORITHM = HASHING_ALGORITHM
        if self.SECRET_KEY is None:
            raise SecretKeyError()
        if self.HASHING_ALGORITHM is None:
            raise HashingAlgorithmError()

    async def verify_password(
        self, plain_password: str, hashed_password: bytes
    ) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password)

    async def hash_password(self, password: str) -> bytes:
        pwd_bytes: bytes = password.encode()
        salt: bytes = bcrypt.gensalt()
        hashed_password: bytes = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    async def generate_jwt_token(self, dict, expiration=TOKEN_EXPIRATION):
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

    async def authenticate_user(
        self, user: LoginUserModel, user_in_db: DBUserModel | None
    ):
        if self.verify_password(user.password, user_in_db.password):
            user_dict = user_in_db.model_dump()
            del user_dict["password"]
            return user_dict
        else:
            raise IncorrectPasswordError()

    async def login(self, user: LoginUserModel):
        with DatabaseInterface() as db:
            if user.email:
                result = await db.get_user_by_email(email=user.email)
            elif user.username:
                result = await db.get_user_by_username(username=user.username)
        if result is None:
            raise UserNotFoundError("User not found")
        else:
            user_dict = await self.authenticate_user(user=user, user_in_db=result)
            token = await self.generate_jwt_token(user_dict)
            return Token(
                access_token=token,
                token_type="bearer",
            )
