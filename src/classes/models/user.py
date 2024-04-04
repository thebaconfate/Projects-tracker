from typing import Any, Optional
from pydantic import BaseModel, EmailStr, model_validator

class BaseUserModel(BaseModel):
    email: EmailStr
    username: str
    password: str

    @model_validator(mode='after')
    def lower(self) -> 'BaseUserModel':
        if self.email:
            self.email = self.email.lower()
        if self.username:
            self.username = self.username.lower()
        return self

class NewUserModel(BaseUserModel):
    pass

class LoginUserModel(BaseUserModel):
    email: Optional[EmailStr]
    username: Optional[str]

    @model_validator(mode='before')
    @classmethod
    def check_existance_email_or_username(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get('email') and not data.get('username'):
                raise ValueError("Either email or username must be provided")
        return data

class DBUserModel(BaseUserModel):
    id: int
