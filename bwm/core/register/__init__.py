import typing as t

from flask import Flask

from .babel import BabelComponent, babel
from .base import Component
from .bcrypt import BcryptComponent, bwm_bcrypt
from .blueprint import BlueprintComponent
from .config import ConfigComponent
from .cors import CORSComponent
from .db import DBComponent, db, migrate
from .errorhandle import ErrorHandlerComponent
from .jwt import JWTComponent, jwt, jwt_redis_blocklist
from .log import LogComponent
from .session import SessionComponent, session

CreateApp = t.Callable[[], Flask]


def register_components(app: Flask, component_list: t.List[Component]):
    """为 flask app 注册组件"""

    for component in component_list:
        component(app).register()

    # 解决循环导入问题
    from bwm import cli, models


__all__ = [
    "BabelComponent",
    "babel",
    "BcryptComponent",
    "bwm_bcrypt",
    "BlueprintComponent",
    "ConfigComponent",
    "CORSComponent",
    "DBComponent",
    "db",
    "migrate",
    "ErrorHandlerComponent",
    "JWTComponent",
    "jwt",
    "jwt_redis_blocklist",
    "LogComponent",
    "SessionComponent",
    "session",
    "register_components",
]
