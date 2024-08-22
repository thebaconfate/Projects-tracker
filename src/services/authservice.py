from datetime import datetime, timedelta, UTC
import logging
import os
from typing import Annotated
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from src.database.interface import DatabaseInterface
from src.errors.authentication import (
    HashingAlgorithmError,
    IncorrectPasswordError,
    SecretKeyError,
    UserNotFoundError,
)
from src.models.user import DBUserModel, LoginUserModel
from src.models.auth import Token


def read_token_expiration():
    token_expiration = os.getenv("TOKEN_EXPIRATION")
    return (
        token_expiration if isinstance(token_expiration, int) else int(token_expiration)
    )


TOKEN_EXPIRATION = read_token_expiration()
SECRET_KEY = os.getenv("SECRET_KEY")
HASHING_ALGORITHM = os.getenv("HASHING_ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(self):
        self.SECRET_KEY = SECRET_KEY
        self.HASHING_ALGORITHM = HASHING_ALGORITHM
        if self.SECRET_KEY is None:
            raise SecretKeyError()
        if self.HASHING_ALGORITHM is None:
            raise HashingAlgorithmError()

    async def verify_password(
        self, plain_password: str, hashed_password: bytearray
    ) -> bool:
        return bcrypt.checkpw(plain_password.encode(), bytes(hashed_password))

    async def hash_password(self, password: str) -> bytes:
        pwd_bytes: bytes = password.encode()
        salt: bytes = bcrypt.gensalt()
        hashed_password: bytes = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    async def generate_jwt_token(self, dict, expiration=TOKEN_EXPIRATION):
        claim = dict.copy()
        expires = datetime.now(UTC) + (
            timedelta(minutes=int(expiration))
            if expiration is not None
            else timedelta(minutes=15)
        )
        claim.update({"exp": expires})
        return jwt.encode(
            payload=claim, key=self.SECRET_KEY, algorithm=self.HASHING_ALGORITHM
        )

    async def get_current_user(
        self, token: Annotated[str, Depends(oauth2_scheme)]
    ) -> DBUserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
        try:
            payload = jwt.decode(
                jwt=token,
                key=self.SECRET_KEY,
                algorithms=[self.HASHING_ALGORITHM],
                options={"require": ["username", "id", "exp"]},
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired"
            )
        except (jwt.PyJWTError, HTTPException, jwt.MissingRequiredClaimError):
            raise credentials_exception
        except Exception as e:
            logging.error(f"Error decoding token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error happened",
            )
        else:
            username: str = payload.get("username")
            user_id: int = payload.get("id")
            async with DatabaseInterface() as db:
                user: DBUserModel | None = await db.get_user_by_username_and_id(
                    username=username, user_id=user_id
                )
            if user is None:
                raise credentials_exception
            else:
                return user

    async def authenticate_user(
        self, user: LoginUserModel, user_in_db: DBUserModel | None
    ):
        logging.debug(f"Authenticating user: {user}")
        if await self.verify_password(user.password, user_in_db.password):
            user_dict = user_in_db.model_dump()
            del user_dict["password"]
            return user_dict
        else:
            raise IncorrectPasswordError()

    async def login(self, user: LoginUserModel):
        logging.debug("Attempting to log in user")
        result = None
        async with DatabaseInterface() as db:
            if user.email:
                result = await db.get_user_by_email(email=user.email)
            elif user.username:
                result = await db.get_user_by_username(username=user.username)
        if result is None:
            logging.debug("User not found")
            raise UserNotFoundError("User not found")
        else:
            logging.debug(f"User found: {result}")
            user_dict = await self.authenticate_user(user=user, user_in_db=result)
            return Token(access_token=await self.generate_jwt_token(user_dict))


authenticated = AuthService().get_current_user
