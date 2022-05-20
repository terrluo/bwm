import typing as t

import redis
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import load_only

from bwm.core.register.base import Component

jwt = JWTManager()

jwt_redis_blocklist: t.Optional[redis.StrictRedis] = None


class JWTComponent(Component):
    def register(self):
        from bwm.account.models import User

        jwt.init_app(self._app)

        global jwt_redis_blocklist
        redis_host = self._app.config["JWT_BLACKLIST_REDIS_HOST"]
        redis_port = self._app.config["JWT_BLACKLIST_REDIS_PORT"]
        redis_db = self._app.config["JWT_BLACKLIST_REDIS_DB"]
        jwt_redis_blocklist = redis.StrictRedis(
            host=redis_host, port=redis_port, db=redis_db, decode_responses=True
        )

        @jwt.user_identity_loader
        def user_identity_lookup(user: User):
            return user.login_id

        @jwt.user_lookup_loader
        def user_lookup_callback(jwt_header, jwt_data) -> t.Optional[User]:
            login_id = jwt_data["sub"]
            return (
                User.query.filter_by(login_id=login_id, is_delete=User.IsDelete.NO)
                .options(load_only(User.login_id, User.username, User.password))
                .first()
            )

        @jwt.token_in_blocklist_loader
        def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
            jti = jwt_payload["jti"]
            revoked_key = self._app.config["JWT_REVOKED_KEY"].format(jti)
            token_in_redis = jwt_redis_blocklist.get(revoked_key)
            return token_in_redis is not None
