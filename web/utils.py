"""
Author: Hugo
Date: 2020-01-07 20:32
Desc:
"""
import os
import time
import hmac

from hashlib import md5
from collections import UserDict
from threading import RLock, Lock

from starlette.config import Config
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory='web/templates')


async def exception_custom(req, exce_info: int):
    template = "exception.html"
    context = {"request": req, "code": exce_info}
    return templates.TemplateResponse(template, context, status_code=401)


async def exception_401(req, exc):
    template = "exception.html"
    context = {"request": req, "code": 401}
    return templates.TemplateResponse(template, context, status_code=401)


async def exception_404(req, exc):
    template = "exception.html"
    context = {"request": req, "code": 404}
    return templates.TemplateResponse(template, context, status_code=404)


async def exception_500(req, exc):
    template = "exception.html"
    context = {"request": req, "code": 500}
    return templates.TemplateResponse(template, context, status_code=500)


def md5_salt(salt: str, encryption_data: str) -> str:
    hash_instance = md5(bytes(salt, encoding="utf-8"))
    hash_instance.update(bytes(encryption_data, encoding="utf-8"))
    v = hash_instance.hexdigest()
    return v


def hmac_salt(salt: str, encryption_data: str) -> str:
    hmac_instance = hmac.new(key=(bytes(salt, encoding="utf-8")), msg=None, digestmod='MD5')
    hmac_instance.update(bytes(encryption_data, encoding="utf-8"))
    v = hmac_instance.hexdigest()
    return v


class TTL(UserDict):
    def __init__(self, *args, **kwargs):
        self._rlock = RLock()
        self._lock = Lock()
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<TTLDict:{} {} '.format(id(self), self.data)

    def __expire__(self, key, ttl, now=None):
        if now is None:
            now = time.time()
        with self._rlock:
            _expire, value = self.data[key]
            self.data[key] = (now + ttl, value)

    def ttl(self, key: str, now=None):
        if now is None:
            now = time.time()
        with self._rlock:
            expire, value = self.data.get(key, (None, None))
            if expire is None:
                return -1
            elif expire <= now:
                del self[key]
                return -2
            return expire - now

    def setex(self, key: str, value: str, ttl: int):
        with self._rlock:
            expire = time.time() + ttl
            self.data[key] = (expire, value)

    def __len__(self):
        with self._rlock:
            for key in list(self.data.keys()):
                self.ttl(key)
            return len(self.data)

    def __iter__(self):
        with self._rlock:
            for k in self.data.keys():
                ttl = self.ttl(k)
                if ttl != -2:
                    yield k

    def __setitem__(self, key, value):
        with self._lock:
            self.data[key] = (None, value)

    def __delitem__(self, key):
        with self._lock:
            del self.data[key]

    def __getitem__(self, key):
        with self._rlock:
            self.ttl(key)
            return self.data[key][1]


def config_info(key: str, default_value=None):
    env = os.getenv("env", "dev")
    config = Config(".env_{}".format(env))
    value = config(key, default=default_value)
    return value


