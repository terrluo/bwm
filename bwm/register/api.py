from flask import current_app, request
from flask_babel import lazy_gettext as _

from bwm import db
from bwm.account.models import User
from bwm.core.errors import ApiError
from bwm.core.restful import Resource, common_marshal, create_route

from .errors import RegisterError
from .schemas import RegisterSchema

register_bp, register_api = create_route(
    "register", __name__, url_prefix="/api/register"
)


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
