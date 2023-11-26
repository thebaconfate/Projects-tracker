from classes.database.databaseinterface import DatabaseInterface
from pydantic import EmailStr
from src.setup import auth


class DuplicateUserException(Exception):
    def __init__(self, message):
        self.message = message


class UserNotFoundException(Exception):
    def __init__(self, message):
        self.message = message


class IncorrectPasswordException(Exception):
    def __init__(self, message):
        self.message = message


class User:
    def __init__(self, email, password, name=None):
        self.email = email
        self.password = password
        self.name = name

    def hash_password(self):
        self.password = auth.hash(self.password)

    def register_user(self):
        with DatabaseInterface() as db:
            user = db.get_user_by_mail(self.email)
            if user == None:
                self.hash_password()
                db.insert_user(self.name, self.email, self.password)
                return RegisteredUser(**self)
            else:
                raise DuplicateUserException("User already exists")

    def __check_password(self, hashed_password):
        return auth.verify(self.password, hashed_password)

    def authenticate_user(self):
        with DatabaseInterface() as db:
            fetched_user = db.get_user_by_mail(self.email)
            if fetched_user == None:
                raise UserNotFoundException("User not found")
            else:
                registered_user = RegisteredUser(**fetched_user)
        if self.__check_password(registered_user.password):
            return registered_user
        else:
            raise IncorrectPasswordException("Incorrect password")


class RegisteredUser:
    def __init__(self, name: str, email: EmailStr, password: str):
        self.name = name
        self.email = email
        self.password = password

    def check_password(self, user: User):
        return auth.verify(user.password, self.password)
