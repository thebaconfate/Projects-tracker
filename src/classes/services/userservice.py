import logging
from fastapi import HTTPException, status
from src.classes.services.authservice import AuthService
from src.classes.errors.database import DatabaseUserAlreadyExistsError
from src.classes.database.interface import DatabaseInterface
from src.classes.models.user import NewUserModel


class UserService:
    def __init__(self, user: NewUserModel):
        """This class does not expect any arguments to be passed to it. It is used to interact with the database to perform operations on the user table."""
        self.user: NewUserModel = user

    async def __hash_password(self, auth: AuthService = AuthService()):
        self.user.password = await auth.hash_password(self.user.password)

    async def add_user(self) -> None:
        """Add a user to the database"""
        try: 
            await self.__hash_password()
            async with DatabaseInterface() as db:
                return await db.save_user(**self.user.model_dump())
        except (DatabaseUserAlreadyExistsError, RuntimeError):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(DatabaseUserAlreadyExistsError().message)
            )
        except Exception as e:
            logging.error(f"Error adding user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )