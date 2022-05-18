import typing as t
from gettext import gettext

from flask import Blueprint, current_app, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
    get_jwt,
    jwt_required,
)
from flask_restful import Api, fields, marshal_with

from bwmv2 import jwt_redis_blocklist
from bwmv2.account.models import User
from bwmv2.core.errors import ApiError
from bwmv2.core.restful import Resource, common_marshal
from bwmv2.login.errors import LoginError

from .schemas import LoginSchema

_ = gettext

login_bp = Blueprint("login", __name__, url_prefix="/api")
login_api = Api(login_bp)


class Login(Resource):
    @marshal_with({"access_token": fields.String(), "refresh_token": fields.String()})
    def post(self):
        data = LoginSchema().load(request.json)
        username: str = data["username"]
        password: str = data["password"]
        user: t.Optional[User] = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            current_app.logger.error(_("用户名或密码错误"))
            raise ApiError.from_error(
                LoginError.USERNAME_PASSWORD_ERROR, http_status=401
            )

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        return {"access_token": access_token, "refresh_token": refresh_token}


class Logout(Resource):
    @common_marshal
    @jwt_required(verify_type=False)
    def post(self):
        token = get_jwt()
        jti: str = token["jti"]
        token_type: str = token["type"]
        revoked_key = current_app.config["JWT_REVOKED_KEY"].format(jti)
        ex = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        jwt_redis_blocklist.set(revoked_key, "", ex=ex)
        return self.success(_(f"撤销{token_type.capitalize()}令牌成功"))


class Refresh(Resource):
    @marshal_with({"access_token": fields.String()})
    @jwt_required(refresh=True)
    def post(self):
        access_token = create_access_token(current_user)
        return {"access_token": access_token}


login_api.add_resource(Login, "/login")
login_api.add_resource(Logout, "/logout")
login_api.add_resource(Refresh, "/refresh")
