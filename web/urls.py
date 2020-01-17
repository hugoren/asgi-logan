"""
Author: Hugo
Date: 2020-01-10 23:23
Desc:
"""

from starlette.routing import Route
from web.endpoint import index
from web.endpoint import login
from web.endpoint import login_check
from web.endpoint import server_info

routes = [
    Route("/", endpoint=index, methods=["GET"]),
    Route("/index", endpoint=index, methods=["GET"]),
    Route("/login", endpoint=login, methods=["GET"]),
    Route("/login/check", endpoint=login_check, methods=["POST"]),
    Route("/api/v1/server/info", endpoint=server_info, methods=["GET"]),
]