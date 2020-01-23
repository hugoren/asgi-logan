"""
Author: Hugo
Date: 23/1/2020 10:37 AM
Desc: 
"""
import os
from starlette.config import Config


def config_info(key: str, default_value=None):
    env = os.getenv("env", "dev")
    config = Config(".env_{}".format(env))
    value = config(key, default=default_value)
    return value
