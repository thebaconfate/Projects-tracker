from flask_login import UserMixin
from src.setup import bcrypt


class User(UserMixin):

    def __init__(self, password, email=None, id=None, name=None, ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User(id={self.id!r}, name={self.name!r})>'.format(self=self)

    def hash_password(self):
        self.password = bcrypt.generate_password_hash(self.password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
