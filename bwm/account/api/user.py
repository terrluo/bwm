from flask import request
from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from bwm.account.service.user import UserService
from bwm.core.restful import Resource, create_route

user_bp, user_api = create_route("user", __name__, url_prefix="/api/user")


class User(Resource):
    @marshal_with(
        {
            "id": fields.Integer(),
            "nickname": fields.String(),
            "username": fields.String(),
            "create_time": fields.DateTime(
                dt_format="iso8601", attribute="local_create_time"
            ),
            "update_time": fields.DateTime(
                dt_format="iso8601", attribute="local_update_time"
            ),
        }
    )
    @jwt_required()
    def get(self):
        return UserService().get_active_user(request.args)


user_api.add_resource(User, "")
