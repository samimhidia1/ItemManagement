# app/models/user.py

from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    hashed_password: str
