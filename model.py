"""
Author: Hugo
Date: 23/1/2020 1:11 PM
Desc: 
"""
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = None


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None


class UserInDB(User):
    hashed_password: str