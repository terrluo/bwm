import logging
import logging.handlers
import os
import re
import typing as t
from datetime import datetime

import redis
from celery import Celery
from dotenv import load_dotenv
from flask import Flask, request
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from .cli import register_cli

load_dotenv()

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

session = Session()

migrate = Migrate()

bwm_bcrypt = Bcrypt()

jwt = JWTManager()

jwt_redis_blocklist: t.Optional[redis.StrictRedis] = None

babel = Babel()

celery = Celery(__name__)
celery.config_from_object("celerytasks.celeryconfig")


def create_app():
    _register_log()

    # 解决循环导入问题
    from . import models

    app = Flask(__name__, instance_relative_config=True)
    _load_config(app)

    CORS(app)

    session.init_app(app)

    db.init_app(app)

    migrate.init_app(app, db=db)

    bwm_bcrypt.init_app(app)

    _register_jwt(app)

    _register_blueprint(app)

    _register_error_handler(app)

    _register_babel(app)

    register_cli(app)

    return app


def _register_log():
    level = os.getenv("BWM_LOG_LEVEL", "INFO").upper()
    log_name = datetime.now().strftime("%Y%m%d%H")

    logging.basicConfig(level=level)
    file_log_handler = logging.handlers.RotatingFileHandler(
        f"logs/{log_name}.log", maxBytes=1024 * 1024 * 10, backupCount=100
    )
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
    )
    file_log_handler.setFormatter(formatter)

    class NoEscape(logging.Filter):
        def __init__(self):
            self.regex = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")

        def strip_esc(self, s):
            try:  # string-like
                return self.regex.sub("", s)
            except Exception:  # non-string-like
                return s

        def filter(self, record: logging.LogRecord) -> bool:
            record.msg = self.strip_esc(record.msg)
            if type(record.args) is tuple:
                record.args = tuple(map(self.strip_esc, record.args))
            return True

    file_log_handler.addFilter(NoEscape())

    logger = logging.getLogger()
    logger.addHandler(file_log_handler)


def _register_babel(app: Flask):
    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        languages: list = app.config.get("LANGUAGES")
        return request.accept_languages.best_match(languages)


def _register_jwt(app: Flask):
    from sqlalchemy.orm import load_only

    from .account.models import User

    jwt.init_app(app)

    global jwt_redis_blocklist
    redis_host = app.config["JWT_BLACKLIST_REDIS_HOST"]
    redis_port = app.config["JWT_BLACKLIST_REDIS_PORT"]
    redis_db = app.config["JWT_BLACKLIST_REDIS_DB"]
    jwt_redis_blocklist = redis.StrictRedis(
        host=redis_host, port=redis_port, db=redis_db, decode_responses=True
    )

    @jwt.user_identity_loader
    def user_identity_lookup(user: User):
        return user.login_id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data) -> t.Optional[User]:
        login_id = jwt_data["sub"]
        return (
            User.query.filter_by(login_id=login_id, is_delete=User.IsDelete.NO)
            .options(load_only(User.login_id, User.username, User.password))
            .first()
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        revoked_key = app.config["JWT_REVOKED_KEY"].format(jti)
        token_in_redis = jwt_redis_blocklist.get(revoked_key)
        return token_in_redis is not None


def _register_error_handler(app: Flask):
    from marshmallow import ValidationError

    from .core.errors import ApiError

    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        for error_msg in e.messages.values():
            return {"message": error_msg[0]}, 400
        return {"message": "未知错误"}, 400

    @app.errorhandler(ApiError)
    def handle_api_error(e: ApiError):
        return e.error, e.http_status


def _register_blueprint(app: Flask):
    """注册蓝图"""
    from .login.api import login_bp
    from .register.api import register_bp
    from .user.api import user_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(user_bp)


def _load_config(app: Flask):
    app.config.from_object("config.default")
    app.config.from_envvar("BWM_CONFIG_FILE")
    instance_config = os.environ.get("INSTANCE_CONFIG")
    if instance_config:
        app.config.from_pyfile(instance_config)


__version__ = "0.1.0"
