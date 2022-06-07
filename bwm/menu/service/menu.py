import typing as t

from bwm.core.schema import load_schema
from bwm.core.service import CacheService
from bwm.menu.schema import AddMenuSchema
from bwm.model import menu


class MenuService(CacheService):
    menu_model = menu.Menu

    def get_all_menu(self, timeout=60 * 60 * 24) -> t.List[menu.Menu]:
        all_menu = self.cache.get("all_menu")
        if not all_menu:
            all_menu = self.menu_model.query.filter(
                self.menu_model.is_delete == self.menu_model.IsDelete.NO
            ).all()
            all_menu = {menu.id: menu for menu in all_menu}
            self.cache.set("all_menu", all_menu, timeout)
        return all_menu

    @load_schema(AddMenuSchema())
    def add_menu(self, data: t.Dict[str, t.Any]):
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
        self.db.session.add(menu)
        self.db.session.commit()
        return menu
