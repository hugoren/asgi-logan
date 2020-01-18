"""
Author: Hugo
Date: 2020-01-07 20:35
Desc:
"""

import uvicorn

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
# from starlette.middleware import Middleware
# from starlette.middleware.trustedhost import TrustedHostMiddleware

from web.urls import routes
from web.utils import exception_401
from web.utils import exception_404
from web.utils import exception_500

from web.endpoint import startup
from web.endpoint import shutdown

"""
   这是0.13.0新版才有的功能
"""
# middleware = [
#   Middleware(TrustedHostMiddleware, allowed_hosts=['*']),
#
# ]

exception_handlers = {
    401: exception_401,
    404: exception_404,
    500: exception_500

}


app = Starlette(routes=routes,
                # middleware=middleware,
                # exception_handlers=exception_handlers,
                # on_startup=[startup],
                # on_shutdown=[shutdown],
                debug=False)


app.mount('/static', StaticFiles(directory='web/statics'), name='static')

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=13000)


