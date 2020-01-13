"""
Author: Hugo
Date: 2020-01-07 14:29
Desc: 
"""

from functools import wraps

from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse

from utils import exception_custom
from utils import hmac_salt

templates = Jinja2Templates(directory='templates')

session_login = {}


async def startup():
    print('Ready to do go')


async def shutdown():
    print('Ready to do down')


def auth(func):
    @wraps(func)
    async def wrap(*args, **kwargs):
        req = args[0]
        if len(args) != 1:
            return await exception_custom(req, 400)
        uid = req.cookies.get("uid")
        if uid not in session_login.keys():
            return await exception_custom(req, 401)
        if uid in session_login.keys():
            # 判断浏览器的环境
            try:
                brower_env = req.scope.get("headers")[6][1]
            except Exception as e:
                brower_env = b"brower_env_1"
            brower_hmac_new = hmac_salt("login_session_$", str(brower_env, encoding="utf-8"))
            brower_hmac_old = session_login.get(uid)
            if brower_hmac_new != brower_hmac_old:
                return await exception_custom(req, 405)
        r = await func(*args, **kwargs)
        return r
    return wrap


@auth
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

    if not username:
        return JSONResponse({"retcode": 1, "stderr": "用户名不能为空"})
    if not password:
        return JSONResponse({"retcode": 1, "stderr": "密码不能为空"})

    username = username.strip()
    password = password.strip()

    if username == "hugo" and password == "boss":

        try:
            brower_env = req.scope.get("headers")[6][1]
        except Exception as e:
            brower_env = b"brower_env_1"
        session_login[hmac_salt("login_session_$", username)] = hmac_salt("login_session_$", str(brower_env, encoding="utf-8"))

        resp = JSONResponse({"retcode": 0, "stdout": "/"})
        try:
            brower_env = req.scope.get("headers")[6][1]
        except Exception as e:
            brower_env = b"brower_env_1"
        resp.set_cookie(key="uid", value=hmac_salt("login_session_$", username),
        max_age=60*60*24*7,
        expires=60*60*24*7,)
        return resp
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
