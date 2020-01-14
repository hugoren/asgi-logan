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
salt = "login_session_$"


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
        username_hash = req.cookies.get("uid")

        # 判断条件1: username_hash 是否存于session
        if username_hash not in session_login.keys():
            return await exception_custom(req, 401)

        # 判断条件2: 浏览器的环境
        user_agent = "user-agent-default"
        headers = req.scope.get("headers")
        if isinstance(headers, (list,)):
            for k, v in headers:
                if k == "user-agent":
                    user_agent = v
        user_agent_hmac_new = hmac_salt(salt, user_agent)
        user_agent_hmac_old = session_login.get(username_hash)
        if user_agent_hmac_new != user_agent_hmac_old:
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

        user_agent = "user-agent-default"
        headers = req.scope.get("headers")
        if isinstance(headers, (list,)):
            for k, v in headers:
                if k == "user-agent":
                    user_agent = v

        # session: key=hash(username), value=hash(user-agent, 客户端的浏览器环境)
        username_hash = hmac_salt(salt, username)
        session_login[username_hash] = hmac_salt(salt, user_agent)

        resp = JSONResponse({"retcode": 0, "stdout": "/"})

        # cookies: key=uid, value=hash(username)
        resp.set_cookie(key="uid", value=username_hash,
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
