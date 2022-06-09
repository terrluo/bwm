import typing as t

from bwm.constants import CacheKey
from bwm.core.schema import load_schema
from bwm.core.service import CacheService
from bwm.menu.schema import AddMenuSchema
from bwm.model import menu
from bwm.type import Data

_Menu = menu.Menu


class MenuService(CacheService):
    model = _Menu

    def get_menu_data(self, timeout=60 * 60 * 24) -> t.Dict[int, Data]:
        key = CacheKey.menu()
        menu_data = self.cache.get(key)
        if menu_data is None:
            menu_list: t.List[_Menu] = self.available.all()
            menu_data = {menu.id: menu.to_dict() for menu in menu_list}
            self.cache.set(key, menu_data, timeout)
        return menu_data

    @load_schema(AddMenuSchema())
    def add_menu(self, data: Data):
        menu = self.model(**data)
        self.db.session.add(menu)
        self.db.session.commit()
        return menu
