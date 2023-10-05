from src.setup import auth
from pydantic import BaseModel

class User(BaseModel):
    def __init__(
        self,
        password,
        email=None,
        id=None,
        name=None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User(id={self.id!r}, name={self.name!r})>".format(self=self)

    def hash_password(self):
        self.password = auth.hash(self.password)

    def check_password(self, password):
        return auth.verify(password, self.password)
