from flask_login import UserMixin
from setup import bcrypt


class User(UserMixin):

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User(id={self.id!r}, name={self.name!r})>'.format(self=self)

    def rehash_password(self):
        self.password = bcrypt.generate_password_hash(self.password)