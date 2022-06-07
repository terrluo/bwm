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

from bwm.account.error import LoginError, RegisterError, UserError
from bwm.account.model import User
from bwm.account.schema import LoginSchema, RegisterSchema
from bwm.core.schema import PageSchema, load_data
from bwm.core.service import Service
from bwm.util.component import get_jwt as util_get_jwt


class UserService(Service):
    user_model = User

    @load_data(PageSchema())
    def get_all_user(self, data):
        page = data["page"]
        limit = data["limit"]

        all_user = self.user_model.query.filter(
            self.user_model.is_delete == self.user_model.IsDelete.NO
        )
        count = all_user.count()
        all_user = self.page(all_user, page, limit).all()
        return dict(data=all_user, count=count)

    def is_exist(self, username: str):
        return self.db.session.query(
            self.user_model.query.filter_by(username=username).exists()
        ).scalar()

    def get_active_user(self, union_id: uuid.UUID) -> t.Optional[User]:
        user: t.Optional[User] = self.user_model.query.filter(
            self.user_model.union_id == str(union_id),
            self.user_model.is_delete == self.user_model.IsDelete.NO,
        ).first()
        if not user:
            current_app.logger.error(_("用户不存在"))
            raise UserError.NOT_FOUND
        return user

    @load_data(RegisterSchema())
    def register(self, data):
        username = data["username"]
        password = data["password"]
        if self.is_exist(data["username"]):
            current_app.logger.error(_("用户已注册"))
            raise RegisterError.REGISTERED

        user = self.user_model(nickname=username, username=username)
        user.union_id = user.generate_union_id()
        user.password = user.generate_password(password)
        self.db.session.add(user)
        self.db.session.commit()

    @load_data(LoginSchema())
    def login(self, data):
        username: str = data["username"]
        password: str = data["password"]
        user: t.Optional[User] = self.user_model.query.filter_by(
            username=username
        ).first()
        if not user or not user.check_password(password):
            current_app.logger.error(_("用户名或密码错误"))
            raise LoginError.USERNAME_PASSWORD_ERROR

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        return {"access_token": access_token, "refresh_token": refresh_token}

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
