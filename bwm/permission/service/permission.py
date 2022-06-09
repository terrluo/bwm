import typing as t

from sqlalchemy import func
from sqlalchemy.engine.row import Row

from bwm.constants import CacheKey
from bwm.core.schema import load_schema
from bwm.core.service import CacheService
from bwm.model import permission
from bwm.permission.schema.permission import AddPermission
from bwm.type import Data

_Permission = permission.Permission


class PermissionService(CacheService):
    model = _Permission

    @load_schema(AddPermission())
    def add_permission(self, data: Data):
        _permission = self.model(
            role_id=data["role_id"],
            menu_id=data["menu_id"],
            is_visible=data["is_visible"],
            is_operate=data["is_operate"],
        )
        self.db.session.add(_permission)
        self.db.session.commit()
        return _permission

    def get_permission_data(self, user_id: int, timeout=60 * 60 * 24):
        key = CacheKey.permission(user_id)
        permission_data: t.Optional[Data] = self.cache.get(key)
        if permission_data is None:
            from bwm.permission.service.role_user import RoleUserService

            role_ids = RoleUserService().get_role_ids(user_id)
            permission_list = (
                self.available.filter(
                    self.model.role_id.in_(role_ids),
                )
                .group_by(
                    self.model.menu_id,
                )
                .with_entities(
                    self.model.menu_id,
                    func.MAX(self.model.is_visible).label("is_visible"),
                    func.MAX(self.model.is_operate).label("is_operate"),
                )
            ).all()
            permission_data = self._handle_permission_data(permission_list)
            self.cache.set(key, permission_data, timeout)

        return permission_data

    def _handle_permission_data(self, permission_list: t.List[Row]):
        from bwm.menu.service.menu import MenuService

        menu_data = MenuService().get_menu_data()
        permission_data = {}
        for perm in permission_list:
            perm_data = perm._asdict()
            menu = menu_data[perm_data["menu_id"]]
            permission_data[menu["route_key"]] = perm_data
        return permission_data
