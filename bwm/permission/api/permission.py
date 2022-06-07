from flask import request
from flask_jwt_extended import jwt_required

from bwm.core.restful import Resource, common_marshal, create_route
from bwm.permission.service.permission import PermissionService

permission_bp, permission_api = create_route(
    "permission", __name__, url_prefix="/api/permission"
)


class Permission(Resource):
    method_decorators = [jwt_required()]

    @common_marshal
    def post(self):
        PermissionService().add_permission(request.json)
        return self.success()


permission_api.add_resource(Permission, "")
