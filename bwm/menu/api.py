from flask import request
from flask_jwt_extended import jwt_required

from bwm.core.restful import Resource, common_marshal, create_route

from .services import MenuService

menu_bp, menu_api = create_route("menu", __name__, url_prefix="/api/menu")


class Menu(Resource):
    method_decorators = [jwt_required()]

    @common_marshal
    def post(self):
        MenuService().add_menu(request.json)
        return self.success()


menu_api.add_resource(Menu, "")
