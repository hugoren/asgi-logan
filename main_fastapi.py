"""
Author: Hugo
Date: 2020-01-17 23:14
Desc: 
"""
import jwt
import json
import uvicorn
from jwt import PyJWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Dict
from fastapi import Header
from model import (
    User, UserInDB, TokenData, Token
)

from utils import config_info

SECRET_KEY = config_info("SALT_KEY")
ALGORITHM = config_info("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config_info("ACCESS_TOKEN_EXPIRE_MINUTES"))

users_db = json.loads(config_info("users_db"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI()


def password_verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def password_hash(password):
    return pwd_context.hash(password)


def user_get(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def user_auth(user_db, username: str, password: str):
    user = user_get(user_db, username)
    if not user:
        return False
    if not password_verify(password, user.hashed_password):
        return False
    return user


def token_create(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def token_explain(data: str) -> Dict:
    try:
        r = jwt.decode(data, SECRET_KEY, algorithm=ALGORITHM)
        return {"retcode": 0, "stdout": r}
    except Exception as e:
        return {"retcode": 1, "stderr": f"{e}"}


async def user_current(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = user_get(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def user_current_active(current_user: User = Depends(user_current)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token/", response_model=Token)
async def token_apply(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_auth(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token_create(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/token/check/")
async def token_check(user: User, access_token: str = Header(None)):
    r = token_explain(access_token)
    return r


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(user_current_active)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(user_current_active)):
    return [{"item_id": "Foo", "owner": current_user.username}]


if __name__ == "__main__":
    print(password_hash("test"))
    uvicorn.run(app=app,
                host="0.0.0.0",
                port=14000,
                workers=1
    )