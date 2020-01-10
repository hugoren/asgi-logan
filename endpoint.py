"""
Author: Hugo
Date: 2020-01-07 14:29
Desc: 
"""

from starlette.templating import Jinja2Templates
from starlette.schemas import SchemaGenerator
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import Response
from starlette.responses import RedirectResponse
from starlette.authentication import SimpleUser

from starlette.authentication import requires

templates = Jinja2Templates(directory='templates')


schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}}
)


async def index(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


async def login(req):
    template = "login.html"
    context = {"request": req}
    return templates.TemplateResponse(template, context)


async def login_check(req):
    data = await req.json()
    username = data.get("username")
    password = data.get("password")
    if username == "hugo" and password == "boss":
        SimpleUser(username)
        return JSONResponse({"retcode": 0, "stdout": "/"})
    return JSONResponse({"retcode": 1, "stderr": "用户信息校验失败"})


async def server_info(req):
    data = {
          "total": 80,
          "totalNotFiltered": 80,
          "rows": [
              {
                "server_id": 0,
                "server_name": "app-test-0",
                "server_status": "online",
                }
          ]
    }

    return JSONResponse(data)


async def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)
