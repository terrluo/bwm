from flask import request
from flask_jwt_extended import jwt_required

from bwm.core.restful import Resource, common_marshal, create_route
from bwm.permission.service.role import RoleService

role_bp, role_api = create_route("role", __name__, url_prefix="/api/role")


class Role(Resource):
    method_decorators = [jwt_required()]

    @common_marshal
    def post(self):
        RoleService().add_role(request.json)
        return self.success()


role_api.add_resource(Role, "")
