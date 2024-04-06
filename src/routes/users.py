import logging
import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.services.userservice import UserService
from src.services.authservice import AuthService
from src.models.user import DBUserModel, LoginUserModel, NewUserModel


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(path=("/login"))
async def login(user: LoginUserModel):
    """Logs a user in by checking the database for a matching username and password"""
    try:
        logging.info(f"Attempting to log in user: {user}")
        token = await AuthService().login(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    else:
        response = Response(
            status_code=status.HTTP_200_OK, content="User logged in successfully"
        )
        response.headers["Authorization"] = f"{token.token_type} {token.access_token}"
        return response


@router.post(path=("/register"))
async def register(user: NewUserModel):
    """Registers a new user by adding them to the database, this requires a unique email address, a username and a password."""
    try:
        await UserService(user).add_user()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    else:
        response = Response(
            status_code=status.HTTP_201_CREATED, content="User registered successfully"
        )
        response.set_cookie(key="username", value=user.username)
        return response

