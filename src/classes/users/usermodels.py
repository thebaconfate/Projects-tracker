from pydantic import BaseModel, EmailStr


class UserRegisterModel(BaseModel):
    email: EmailStr
    password: str


class RegisteredUserModel(BaseModel):
    email: EmailStr
    password: str


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str


class UserLogoutModel(BaseModel):
    email: EmailStr
    password: str
