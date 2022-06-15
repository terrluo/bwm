import typing as t

from celery import Celery
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_session import Session

from .babel import BabelComponent
from .base import Component
from .blueprint import BlueprintComponent
from .config import ConfigComponent
from .db import DBComponent
from .errorhandle import ErrorHandlerComponent
from .jwt import JWTComponent
from .log import LogComponent
from .marshmallow import MarshmallowComponent

cache = Cache()
celery = Celery(__name__)
celery.config_from_object("celerytask.celeryconfig")
bcrypt = Bcrypt()


def register_components(app: Flask, component_list: t.List[Component]):
    """为 flask app 注册组件"""

    for component in component_list:
        component(app).register()

    CORS(app)
    Session(app)
    cache.init_app(app)
    bcrypt.init_app(app)

    # 解决循环导入问题
    from bwm import cli, model  # noqa


__all__ = [
    "BabelComponent",
    "bcrypt",
    "BlueprintComponent",
    "cache",
    "ConfigComponent",
    "celery",
    "DBComponent",
    "ErrorHandlerComponent",
    "JWTComponent",
    "LogComponent",
    "MarshmallowComponent",
    "register_components",
]
