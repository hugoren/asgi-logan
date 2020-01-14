"""
Author: Hugo
Date: 2020-01-07 09:35
Desc: 
"""

import uvicorn

from urls import routes

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from utils import exception_401
from utils import exception_404
from utils import exception_500

from endpoint import startup
from endpoint import shutdown


middleware = [
  Middleware(TrustedHostMiddleware, allowed_hosts=['*']),

]

exception_handlers = {
    401: exception_401,
    404: exception_404,
    500: exception_500

}


app = Starlette(routes=routes,
                middleware=middleware,
                exception_handlers=exception_handlers,
                on_startup=[startup],
                on_shutdown=[shutdown],
                debug=False)
app.mount('/static', StaticFiles(directory='statics'), name='static')


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=13000)


