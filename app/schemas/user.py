
import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    phone: str | None = Field(default=None, max_length=20)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Name must contain at least 2 characters")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
            raise ValueError("Password must contain at least one letter and one number")
        return value


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)



class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"






# UserCreate validates registration input before it reaches your database.
# EmailStr validates email format. It requires the email-validator package.
# Passwords must be at least 12 characters and include a letter and a number
# UserResponse exposes safe user fields, never the password or its hash.
# from_attributes=True lets Pydantic build the response from a SQLAlchemy model.
# UserLogin validates the credentials, while TokenResponse defines the response containing the access token.
