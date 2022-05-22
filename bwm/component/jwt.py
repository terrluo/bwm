import typing as t

import redis
from flask import Flask, session
from flask_babel import lazy_gettext as _
from flask_jwt_extended import JWTManager as _JWTManager
from sqlalchemy.orm import load_only

from bwm.component.base import Component


class JWTComponent(Component):
    def register(self):
        from bwm.account.models import User

        jwt.init_app(self._app)

        @jwt.user_identity_loader
        def user_identity_lookup(user: User):
            return user.login_id

        @jwt.user_lookup_loader
        def user_lookup_callback(jwt_header, jwt_data) -> t.Optional[User]:
            login_id = jwt_data["sub"]
            user: t.Optional[User] = session.get(login_id)
            if not user:
                user = (
                    User.query.filter_by(login_id=login_id, is_delete=User.IsDelete.NO)
                    .options(load_only(User.login_id, User.username, User.password))
                    .first()
                )
                session[login_id] = user
            return user

        @jwt.token_in_blocklist_loader
        def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
            jti = jwt_payload["jti"]
            revoked_key = self._app.config["JWT_REVOKED_KEY"].format(jti)
            token_in_redis = jwt.redis_blocklist.get(revoked_key)
            return token_in_redis is not None


class JWTManager(_JWTManager):
    def __init__(self, app: Flask = None) -> None:
        super().__init__(app)
        self._redis_blocklist: t.Optional[redis.StrictRedis] = None

    def init_app(self, app: Flask) -> None:
        super().init_app(app)

        redis_host = app.config["JWT_BLACKLIST_REDIS_HOST"]
        redis_port = app.config["JWT_BLACKLIST_REDIS_PORT"]
        redis_db = app.config["JWT_BLACKLIST_REDIS_DB"]
        self._redis_blocklist = redis.StrictRedis(
            host=redis_host, port=redis_port, db=redis_db, decode_responses=True
        )

    @property
    def redis_blocklist(self):
        if not self._redis_blocklist:
            raise RuntimeError(_("redis_blocklist 未初始化"))
        return self._redis_blocklist


jwt = JWTManager()
