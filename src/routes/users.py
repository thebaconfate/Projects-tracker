import os
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from src.classes.models.auth import Token
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
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
    except Exception as e:
        return {"message": str(e)}
    finally:
        auth = AuthService()
        auth_user = await auth.authenticate_user(user=user, user_in_db=result)
        if auth_user:
            token = Token(
                access_token=await auth.generate_jwt_token(auth_user),
                token_type="bearer",
            )
            response = JSONResponse(content="Authentication succesful")
            response.set_cookie(key=token.token_type, value=token.access_token)
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
