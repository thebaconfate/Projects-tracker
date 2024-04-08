from typing import Any, Optional
from pydantic import BaseModel, EmailStr, model_validator, field_validator


class BaseUserModel(BaseModel):
    email: EmailStr
    username: str
    password: str

    @model_validator(mode="before")
    @classmethod
    def lower(cls, data: Any):
        if isinstance(data, dict):
            if data.get("email"):
                data["email"] = data["email"].lower()
            if data.get("username"):
                data["username"] = data["username"].lower()
            return data


class NewUserModel(BaseUserModel):
    pass


class LoginUserModel(BaseUserModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_existance_email_or_username(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("email") and not data.get("username"):
                raise ValueError("Either email or username must be provided")
            else:
                return data


class DBUserModel(BaseUserModel):
    id: int
    password: bytes

    @field_validator("password", mode="before")
    def validate_byte_data(cls, value):
        if isinstance(value, bytearray):
            return bytes(value)
        elif isinstance(value, bytes):
            return value
        elif isinstance(value, str):
            return value.encode()
        else:
            raise ValueError("Invalid data type for bytes")
