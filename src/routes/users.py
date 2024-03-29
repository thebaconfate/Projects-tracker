import os
from fastapi import APIRouter

from src.classes.services.authservice import AuthService
from src.classes.models.user import UserModel
from src.classes.database.interface import DatabaseInterface


async def get_secret_key() -> str:
    return os.getenv(key="SECRET_KEY")


async def get_hashing_algorithm() -> str:
    return os.getenv(key="HASHING_ALGORITHM")


async def get_token_expiration() -> int:
    return int(os.getenv(key="TOKEN_EXPIRATION"))


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(path=("/login"))
async def login(user: UserModel):
    """Logs a user in by checking the database for a matching username and password"""
    try:
        async with DatabaseInterface() as db:
            if user.email is not None:
                result = await db.get_user_by_email(email=user.email)
            elif user.username is not None:
                result = await db.get_user_by_username(username=user.username)
            else:
                result = {"message": "No email or username provided"}
    except Exception as e:
        return {"message": str(e)}
    finally:
        return await AuthService().authenticate_user(user=user, user_in_db=result)
