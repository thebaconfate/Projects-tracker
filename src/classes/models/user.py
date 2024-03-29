from pydantic import BaseModel


class UserModel(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str


class UserDBModel(UserModel):
    id: int
