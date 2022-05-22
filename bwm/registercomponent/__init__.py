import typing as t

from celery import Celery
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session

from .babel import BabelComponent, babel
from .base import Component
from .blueprint import BlueprintComponent
from .config import ConfigComponent
from .db import DBComponent, db, migrate
from .errorhandle import ErrorHandlerComponent
from .jwt import JWTComponent, jwt
from .log import LogComponent

celery = Celery(__name__)
celery.config_from_object("celerytasks.celeryconfig")
bwm_bcrypt = Bcrypt()


def register_components(app: Flask, component_list: t.List[Component]):
    """为 flask app 注册组件"""

    for component in component_list:
        component(app).register()

    CORS(app)
    Session(app)
    bwm_bcrypt.init_app(app)

    # 解决循环导入问题
    from bwm import cli, models


__all__ = [
    "BabelComponent",
    "babel",
    "bwm_bcrypt",
    "BlueprintComponent",
    "ConfigComponent",
    "celery",
    "DBComponent",
    "db",
    "migrate",
    "ErrorHandlerComponent",
    "JWTComponent",
    "jwt",
    "LogComponent",
    "register_components",
]
