from gettext import gettext

from flask import Blueprint, current_app, request
from flask_restful import Api

from bwmv2 import db
from bwmv2.account.models import User
from bwmv2.core.api import Resource, common_marshal
from bwmv2.core.errors import ApiError

from .errors import RegisterError
from .schemas import RegisterSchema

_ = gettext

register_bp = Blueprint("register", __name__, url_prefix="/api/register")
register_api = Api(register_bp)


class Register(Resource):
    @common_marshal
    def post(self):
        data = RegisterSchema().load(request.json)

        username = data["username"]
        password = data["password"]
        if User.is_exist(data["username"]):
            current_app.logger.error(_("用户已注册"))
            raise ApiError.from_error(RegisterError.REGISTERED)

        login_id = User.generate_login_id()
        pw_hash = User.generate_password(password)
        user = User(
            login_id=login_id, nickname=username, username=username, password=pw_hash
        )
        db.session.add(user)
        db.session.commit()
        return self.success(_("注册成功"))


register_api.add_resource(Register, "/")
