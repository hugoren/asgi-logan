"""
Author: Hugo
Date: 2020-01-07 21:29
Desc: 
"""
import time
from functools import wraps

from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse

from utils import TTL
from utils import config_info
from utils import hmac_salt
from utils import exception_custom

from service import audit_record

from model import db
templates = Jinja2Templates(directory='templates')

SESSION = TTL()
EXPIRE = int(config_info("expire"))
SALT = config_info("salt")


async def startup():
    db.connect()
    print('Ready to do go')


async def shutdown():
    db.close()
    print('Ready to do down')


def auth(func):
    @wraps(func)
    async def wrap(*args, **kwargs):
        req = args[0]
        if len(args) != 1:
            return await exception_custom(req, 400)
        username_hash = req.cookies.get("uid")

        # 判断条件1: username_hash 是否过期
        if username_hash not in SESSION.keys():
            return await exception_custom(req, 401)

        # 判断条件2: 浏览器的环境(或client_ip)
        user_agent = "user-agent-default"
        headers = req.scope.get("headers")
        if isinstance(headers, (list,)):
            for k, v in headers:
                if k == "user-agent":
                    user_agent = v
        user_agent_hmac_new = hmac_salt(SALT, user_agent)
        user_agent_hmac_old = SESSION.get(username_hash)
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

    if username == config_info("username") and password == config_info("password"):

        # 审计记录
        await audit_record(event=f"{username}登陆", event_type="login", level=1, timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))

        # session: key=hash(username), value=hash(user-agent, 客户端的浏览器环境)
        user_agent = "user-agent-default"
        headers = req.scope.get("headers")
        if isinstance(headers, (list,)):
            for k, v in headers:
                if k == "user-agent":
                    user_agent = v

        username_hash = hmac_salt(SALT, username)
        SESSION.setex(key=username_hash, value=hmac_salt(SALT, user_agent), ttl=EXPIRE)

        resp = JSONResponse({"retcode": 0, "stdout": "/"})

        # cookies: key=uid, value=hash(username)
        resp.set_cookie(key="uid", value=username_hash,
                        max_age=EXPIRE,
                        expires=EXPIRE,
                        path="/",
                        domain=None,
                        # 只允许在https访问
                        secure=False,
                        # 防止xss
                        httponly=True,
        )
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
