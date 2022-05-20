from gettext import gettext

from flask import current_app
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from bwm.account.models import User as UserModel
from bwm.core.errors import ApiError
from bwm.core.restful import Resource, create_route
from bwm.user.errors import UserError

_ = gettext

user_bp, user_api = create_route("user", __name__, url_prefix="/api/user")


class User(Resource):
    @marshal_with(
        {
            "id": fields.Integer(),
            "nickname": fields.String(),
            "username": fields.String(),
            "create_time": fields.DateTime(dt_format="iso8601"),
            "update_time": fields.DateTime(dt_format="iso8601"),
        }
    )
    @jwt_required()
    def get(self, user_id: int):
        user = UserModel.get_active_user(user_id)
        if not user:
            current_app.logger.error(_("用户不存在"))
            raise ApiError.from_error(UserError.NOT_FOUND)
        return user


user_api.add_resource(User, "/<int:user_id>")
