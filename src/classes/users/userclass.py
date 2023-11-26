from classes.database.databaseinterface import DatabaseInterface
from pydantic import EmailStr
from src.setup import auth

class DuplicateUserException(Exception):
    def __init__(self, message):
        self.message = message

class UserNotFoundException(Exception):
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

    def check_password(self):
        with DatabaseInterface() as db:
            user = db.get_user_by_mail(self.email)
            if user == None:
                raise UserNotFoundException("User not found")
            else:
                registered_user = RegisteredUser(**user)
                return registered_user.check_password(self)


class RegisteredUser:
    def __init__(self, name: str, email: EmailStr, password: str):
        self.name = name
        self.email = email
        self.password = password

    def check_password(self, login_user: User):
        return auth.verify(login_user.password, self.password)
