import logging
from fastapi import HTTPException, status
from src.services.authservice import AuthService
from src.errors.database import DatabaseUserAlreadyExistsError
from src.database.interface import DatabaseInterface
from src.models.user import NewUserModel


class UserService:
    def __init__(self, user: NewUserModel):
        self.user: NewUserModel = user

    async def __hash_password(self, auth: AuthService = AuthService()):
        return await auth.hash_password(self.user.password)

    async def add_user(self) -> None:
        """Add a user to the database"""
        try:
            async with DatabaseInterface() as db:
                return await db.save_user(
                    username=self.user.username,
                    email=self.user.email,
                    password=await self.__hash_password(),
                )
        except (DatabaseUserAlreadyExistsError, RuntimeError):
            """RuntimeError added because the exception is being raised when a set size changes during iteration and I have no idea what causes it."""
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(DatabaseUserAlreadyExistsError().message),
            )
        except Exception as e:
            logging.error(f"Error adding user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error ocurred",
            )
