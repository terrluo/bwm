from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import fields, marshal_with

from bwm.account.service.user import UserService
from bwm.core.restful import Resource, create_route, marshal_list

user_bp, user_api = create_route("user", __name__, url_prefix="/api/user")


user_info = {
    "nickname": fields.String(),
    "username": fields.String(),
    "create_time": fields.DateTime(dt_format="iso8601", attribute="local_create_time"),
    "update_time": fields.DateTime(dt_format="iso8601", attribute="local_update_time"),
}


class User(Resource):
    method_decorators = [jwt_required()]

    @marshal_with(user_info)
    def get(self):
        return current_user


class UserList(Resource):
    method_decorators = [jwt_required()]

    @marshal_with(marshal_list(user_info))
    def get(self):
        return UserService().get_all_user(request.args)


user_api.add_resource(User, "")
user_api.add_resource(UserList, "")
