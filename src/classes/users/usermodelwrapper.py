from usermodels import RegisteredUserModel
from src.setup import auth


class User:
    def __init__(self, user):
        self.email = user.email
        self.password = user.password

    def hash_password(self):
        self.password = auth.hash(self.password)


class RegisteredUser:
    def __init__(self, user: RegisteredUserModel):
        self.password = user.password

    def check_password(self, login_user: User):
        return auth.verify(login_user.password, self.password)
