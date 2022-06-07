from flask import request
from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from bwm.account.service.user import UserService
from bwm.core.restful import Resource, common_marshal, create_route

login_bp, login_api = create_route("login", __name__, url_prefix="/api")


class Login(Resource):
    @marshal_with(
        {
            "access_token": fields.String(),
            "refresh_token": fields.String(),
        }
    )
    def post(self):
        return UserService().login(request.json)


class Logout(Resource):
    @common_marshal
    @jwt_required(verify_type=False)
    def post(self):
        token = UserService().logout()
        token_type: str = token["type"]
        return self.success(_("撤销%(token_type)s令牌成功", token_type=token_type))


class Refresh(Resource):
    @marshal_with({"access_token": fields.String()})
    @jwt_required(refresh=True)
    def post(self):
        access_token = UserService().refresh()
        return {"access_token": access_token}


login_api.add_resource(Login, "/login")
login_api.add_resource(Logout, "/logout")
login_api.add_resource(Refresh, "/refresh")
