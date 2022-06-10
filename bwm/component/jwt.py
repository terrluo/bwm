import typing as t

import redis
from flask import Flask, request, session
from flask_babel import lazy_gettext as _
from flask_jwt_extended import JWTManager as _JWTManager

from bwm.component.base import Component
from bwm.type import Data


class JWTComponent(Component):
    def register(self):
        from bwm.model import account

        jwt.init_app(self._app)

        @jwt.user_identity_loader
        def user_identity_lookup(user: account.User):
            return str(user.union_id)

        @jwt.user_lookup_loader
        def user_lookup_callback(
            jwt_header: dict, jwt_data: dict
        ) -> t.Optional[account.User]:
            return _get_login_user(jwt_data)

        @jwt.token_in_blocklist_loader
        def check_if_token_is_revoked(jwt_header: dict, jwt_data: dict):
            jti = jwt_data["jti"]
            revoked_key = self._app.config["JWT_REVOKED_KEY"].format(jti)
            token_in_redis = jwt.redis_blocklist.get(revoked_key)
            return token_in_redis is not None

        @jwt.token_verification_loader
        def token_verification(jwt_header: dict, jwt_data: dict):
            user = _get_login_user(jwt_data)
            if user is not None and self._app.config.get("GLOBAL_PERMISSION_CHECK"):
                user.check_permission(request.endpoint, request.method)
                return True
            return False

        def _get_login_user(jwt_data: dict):
            union_id = jwt_data["sub"]
            user_data: Data = session.get(union_id)
            if user_data is None:
                user: t.Optional[account.User] = account.User.query.filter_by(
                    union_id=union_id, is_delete=False
                ).first()
                if user:
                    session[union_id] = user.to_dict()
            else:
                user = account.User(**user_data)
            return user


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
