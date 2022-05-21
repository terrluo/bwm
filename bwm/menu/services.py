import typing as t

from flask import current_app

from bwm.core.error import ApiError
from bwm.core.schema import load_data
from bwm.registercomponent import db

from .errors import MenuError
from .models import Menu
from .schemas import AddMenuSchema


class MenuService:
    menu_model = Menu

    @load_data(AddMenuSchema())
    def add_menu(self, data: t.Dict[str, t.Any]):
        self._add_menu_check(data)

        menu_name = data["menu_name"]
        menu_order = data["menu_order"]
        menu_type = data["menu_type"]
        parent_id = data["parent_id"]
        route_key = data["route_key"]
        is_visible = data["is_visible"]
        menu = self.menu_model(
            menu_name=menu_name,
            menu_order=menu_order,
            menu_type=menu_type,
            parent_id=parent_id,
            route_key=route_key,
            is_visible=is_visible,
        )
        db.session.add(menu)
        db.session.commit()
        return menu

    @load_data(AddMenuSchema(partial={"menu_order", "is_visible"}))
    def _add_menu_check(self, data: t.Dict[str, t.Any]):
        parent_id = data["parent_id"]
        menu_type = data["menu_type"]
        menu_name = data["menu_name"]
        route_key = data["route_key"]

        endpoint, _ = self.unpack_route_key(route_key)
        try:
            current_app.url_map.iter_rules(endpoint)
        except KeyError:
            raise ApiError.from_error(MenuError.ROUTE_NOT_FOUND)

        is_exist = db.session.query(
            self.menu_model.query.filter_by(
                parent_id=parent_id, menu_type=menu_type, menu_name=menu_name
            ).exists()
        ).scalar()
        if is_exist:
            raise ApiError.from_error(MenuError.EXISTED)

    def unpack_route_key(self, route_key: str):
        endpoint, method = route_key.split("#", 2)
        return endpoint, method
