import typing as t

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
from bwm.account.schema import LoginSchema, RegisterSchema, UserSchema
from bwm.component import jwt
from bwm.core.schema import load_data
from bwm.core.service import Service


class UserService(Service):
    user_model = User

    def is_exist(self, username: str):
        return self.db.session.query(
            self.user_model.query.filter_by(username=username).exists()
        ).scalar()

    @load_data(UserSchema())
    def get_active_user(self, data) -> t.Optional[User]:
        user_id: int = data["user_id"]
        user: t.Optional[User] = self.user_model.query.filter(
            self.user_model.id == user_id,
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
        user.login_id = user.generate_login_id()
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
        login_id: str = token["sub"]
        jti: str = token["jti"]
        revoked_key = current_app.config["JWT_REVOKED_KEY"].format(jti)
        ex = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        jwt.redis_blocklist.set(revoked_key, "", ex=ex)
        session.pop(login_id, None)
        return token

    def refresh(self):
        return create_access_token(current_user)
