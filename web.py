"""
Author: Hugo
Date: 2020-01-07 09:35
Desc: 
"""

import uvicorn
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from urls import routes
from utils import BasicAuthBackend
from utils import on_auth_error


middleware = [
  Middleware(TrustedHostMiddleware, allowed_hosts=['*']),
  #Middleware(AuthenticationMiddleware, backend=BasicAuthBackend(), on_error=on_auth_error)
]

app = Starlette(routes=routes, middleware=middleware, debug=False)
app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend(), on_error=on_auth_error)
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='statics'), name='static')


@app.route('/error')
async def error(req):
    template = "exception.html"
    context = {"request": req, "code": 500}
    return templates.TemplateResponse(template, context, status_code=500)


@app.exception_handler(401)
async def not_found_401(req, exc):
    template = "exception.html"
    context = {"request": req, "code": 401}
    return templates.TemplateResponse(template, context, status_code=401)


@app.exception_handler(404)
async def not_found(req, exc):
    template = "exception.html"
    context = {"request": req, "code": 404}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(req, exc):
    template = "exception.html"
    context = {"request": req, "code": 500}
    return templates.TemplateResponse(template, context, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=13000)


