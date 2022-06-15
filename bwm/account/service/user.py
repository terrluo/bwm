import typing as t
import uuid

from flask import current_app, session
from flask_babel import lazy_gettext as _
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
    get_jwt,
)

from bwm.account.error.login import LoginError
from bwm.account.error.register import RegisterError
from bwm.account.error.user import UserError
from bwm.account.schema.login import LoginSchema
from bwm.account.schema.register import RegisterSchema
from bwm.account.schema.user import ChangeOwnPasswordSchema
from bwm.core.schema import PageSchema, load_schema
from bwm.core.service import Service
from bwm.model import account
from bwm.type import Data
from bwm.util.component import get_jwt as util_get_jwt

_User = account.User


class UserService(Service):
    model = _User

    @load_schema(ChangeOwnPasswordSchema())
    def change_own_password(self, data: Data):
        user: _User = data["user"]
        new_password = data["new_password"]
        user.change_password(new_password)
        self.db.session.commit()
        self.logout()

    @load_schema(PageSchema())
    def get_all_user(self, data: Data):
        page = data["page"]
        limit = data["limit"]

        all_user = self.available
        count = all_user.count()
        all_user = self.page(all_user, page, limit).all()
        return dict(data=all_user, count=count)

    def is_exist(self, username: str):
        return self.db.session.query(
            self.model.query.filter_by(username=username).exists()
        ).scalar()

    def get_active_user(self, union_id: uuid.UUID) -> t.Optional[_User]:
        user: t.Optional[_User] = self.available.filter(
            self.model.union_id == str(union_id),
        ).first()
        if not user:
            current_app.logger.error(_("用户不存在"))
            raise UserError.NOT_FOUND
        return user

    @load_schema(RegisterSchema())
    def register(self, data):
        username = data["username"]
        password = data["password"]
        if self.is_exist(data["username"]):
            current_app.logger.error(_("用户已注册"))
            raise RegisterError.REGISTERED

        user = self.model(nickname=username, username=username)
        user.password = user.generate_password(password)
        self.db.session.add(user)
        self.db.session.commit()

    @load_schema(LoginSchema())
    def login(self, data):
        username: str = data["username"]
        password: str = data["password"]
        user: t.Optional[_User] = self.available.filter_by(username=username).first()
        if not user or not user.check_password(password):
            current_app.logger.error(_("用户名或密码错误"))
            raise LoginError.USERNAME_PASSWORD_ERROR

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def logout(self):
        token = get_jwt()
        union_id: str = token["sub"]
        jti: str = token["jti"]
        revoked_key = current_app.config["JWT_REVOKED_KEY"].format(jti)
        ex = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        util_get_jwt().redis_blocklist.set(revoked_key, "", ex=ex)
        session.pop(union_id, None)
        return token

    def refresh(self):
        return create_access_token(current_user)
