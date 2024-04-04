import logging
import os
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse

from src.classes.errors.database import DatabaseConnectionError, DatabaseUserAlreadyExistsError
from src.classes.models.auth import Token
from src.classes.services.authservice import AuthService
from src.classes.models.user import UserModel
from src.classes.database.interface import DatabaseInterface

router_prefix = "/users"


async def get_secret_key() -> str:
    return os.getenv(key="SECRET_KEY")


async def get_hashing_algorithm() -> str:
    return os.getenv(key="HASHING_ALGORITHM")


async def get_token_expiration() -> int:
    return int(os.getenv(key="TOKEN_EXPIRATION"))


router = APIRouter(
    prefix=router_prefix,
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(path=("/login"))
async def login(user: UserModel):
    """Logs a user in by checking the database for a matching username and password"""
    error_detail = "Incorrect username or password"
    error_header = {"WWW-Authenticate": "Bearer"}
    try:
        async with DatabaseInterface() as db:
            if user.email is not None:
                user.email = user.email.lower()
                result = await db.get_user_by_email(email=user.email)
            elif user.username is not None:
                user.username = user.username.lower()
                result = await db.get_user_by_username(username=user.username.lower())
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No username or email provided",
                    headers=error_header,
                )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
            headers=error_header,
        )
    else:
        auth = AuthService()
        auth_user = await auth.authenticate_user(user=user, user_in_db=result)
        if auth_user:
            token = Token(
                access_token=await auth.generate_jwt_token(auth_user),
                token_type="bearer",
            )
            response = JSONResponse(content="Authentication successful")
            response.set_cookie(key=token.token_type, value=token.access_token)
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_detail,
                headers=error_header,
            )


@router.post(path=("/register"))
async def register(user: UserModel):
    """Registers a new user by adding them to the database"""
    if user.email and user.username:
        try:
            async with DatabaseInterface() as db:
                auth = AuthService()
                user.email = user.email.lower()
                user.username = user.username.lower()
                user.password = await auth.hash_password(user.password)
                await db.save_user(**user.model_dump())
        except (DatabaseUserAlreadyExistsError, RuntimeError):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(DatabaseUserAlreadyExistsError().message),
            )
        except DatabaseConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
        except Exception as e:
            logging.ERROR(msg=f"An unknown error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="an unknown error occurred",
            )
        else:
            return RedirectResponse(
                url=f"{router_prefix}/login",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and email required",
        )
