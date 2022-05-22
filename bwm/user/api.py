from flask import current_app, request
from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from bwm.account.models import User as UserModel
from bwm.core.restful import Resource, create_route

from .errors import UserError
from .schemas import UserSchema

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
        data = UserSchema().load(request.args)
        user_id = data.get("user_id")
        user = UserModel.get_active_user(user_id)
        if not user:
            current_app.logger.error(_("用户不存在"))
            raise UserError.NOT_FOUND
        return user


user_api.add_resource(User, "")
