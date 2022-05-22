import typing as t

import redis
from flask import current_app, g, session
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import load_only

from bwm.registercomponent.base import Component

jwt = JWTManager()


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
            token_in_redis = get_jwt_redis_blocklist().get(revoked_key)
            return token_in_redis is not None


def get_jwt_redis_blocklist():
    blocklist = getattr(g, "jwt_redis_blocklist", None)
    if not blocklist:
        redis_host = current_app.config["JWT_BLACKLIST_REDIS_HOST"]
        redis_port = current_app.config["JWT_BLACKLIST_REDIS_PORT"]
        redis_db = current_app.config["JWT_BLACKLIST_REDIS_DB"]
        blocklist = redis.StrictRedis(
            host=redis_host, port=redis_port, db=redis_db, decode_responses=True
        )
        g.jwt_redis_blocklist = blocklist
    return blocklist
