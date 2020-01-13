"""
Author: Hugo
Date: 2020-01-07 14:32
Desc: 
"""

from pydantic import BaseModel
from starlette.templating import Jinja2Templates

from starlette.authentication import (
        AuthenticationBackend, AuthenticationError,
        SimpleUser, UnauthenticatedUser,
         AuthCredentials
)


from starlette.requests import Request
from starlette.responses import JSONResponse


import base64
import binascii

templates = Jinja2Templates(directory='templates')


class CustomAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        # TODO: You'd want to verify the username and password here.
        print(username, password)
        return AuthCredentials(["authenticated"]), SimpleUser(username)


def on_auth_error(request: Request, exc: Exception):
    print("401")
    return JSONResponse({"error": str(exc)}, status_code=401)


async def exception_custom(req, exce_info: int):
    template = "exception.html"
    context = {"request": req, "code": exce_info}
    return templates.TemplateResponse(template, context, status_code=401)


async def exception_401(req, exc):
    template = "exception.html"
    context = {"request": req, "code": 401}
    return templates.TemplateResponse(template, context, status_code=401)


async def exception_404(req, exc):
    template = "exception.html"
    context = {"request": req, "code": 404}
    return templates.TemplateResponse(template, context, status_code=404)


async def exception_500(req, exc):
    template = "exception.html"
    context = {"request": req, "code": 500}
    return templates.TemplateResponse(template, context, status_code=500)


import hmac
from hashlib import md5


def md5_salt(salt: str, encryption_data: str) -> str:
    hash_instance = md5(bytes(salt, encoding="utf-8"))
    hash_instance.update(bytes(encryption_data, encoding="utf-8"))
    v = hash_instance.hexdigest()
    return v


def hmac_salt(salt: str, encryption_data: str) -> str:
    hmac_instance = hmac.new(key=(bytes(salt, encoding="utf-8")), msg=None, digestmod='MD5')
    hmac_instance.update(bytes(encryption_data, encoding="utf-8"))
    v = hmac_instance.hexdigest()
    return v



