"""
Author: Hugo
Date: 2020-01-10 10:23
Desc: 
"""

from starlette.routing import Route
from endpoint import index
from endpoint import login
from endpoint import login_check
from endpoint import server_info

routes = [
    Route("/", endpoint=index, methods=["GET"]),
    Route("/index", endpoint=index, methods=["GET"]),
    Route("/login", endpoint=login, methods=["GET"]),
    Route("/login/check", endpoint=login_check, methods=["POST"]),
    Route("/api/v1/server/info", endpoint=server_info, methods=["GET"]),
]