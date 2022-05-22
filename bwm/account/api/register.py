from flask import current_app, request
from flask_babel import lazy_gettext as _

from bwm.account.service.user import UserService
from bwm.core.restful import Resource, common_marshal, create_route

register_bp, register_api = create_route(
    "register", __name__, url_prefix="/api/register"
)


class Register(Resource):
    @common_marshal
    def post(self):
        UserService().register(request.json)
        return self.success(_("注册成功"))


register_api.add_resource(Register, "/")
