from pydantic import BaseModel, EmailStr, model_validator
from userclass import User


class UserModel(BaseModel):
    name: str | None
    email: EmailStr
    password: str

    @model_validator(mode="after")
    def validate(self):
        return User(**self)
