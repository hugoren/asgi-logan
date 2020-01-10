"""
Author: Hugo
Date: 2020-01-07 14:32
Desc: 
"""

from starlette.authentication import (
        AuthenticationBackend, AuthenticationError,
        SimpleUser, UnauthenticatedUser,
         AuthCredentials
)

from starlette.requests import Request
from starlette.responses import JSONResponse


import base64
import binascii


class BasicAuthBackend(AuthenticationBackend):
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