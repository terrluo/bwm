import typing as t

from bwm.constants import CacheKey
from bwm.core.schema import load_schema
from bwm.core.service import CacheService
from bwm.model import permission
from bwm.permission.schema.permission import AddPermission, GetPermission
from bwm.type import ServiceData


class PermissionService(CacheService):
    model = permission.Permission

    @load_schema(AddPermission())
    def add_permission(self, data: ServiceData):
        _permission = self.model(
            role_id=data["role_id"],
            menu_id=data["menu_id"],
            is_visible=data["is_visible"],
            is_operate=data["is_operate"],
        )
        self.db.session.add(_permission)
        self.db.session.commit()
        return _permission

    @load_schema(GetPermission())
    def get_permission(self, data: ServiceData, timeout=60 * 60 * 24):
        role_id = data["role_id"]
        menu_id = data["menu_id"]
        key = CacheKey.permission(role_id)
        all_permission = self.cache.get(key)
        if all_permission is None:
            permission_list: t.List[permission.Permission] = self.model.query.filter_by(
                role_id=role_id, is_delete=self.model.IsDelete.NO
            )
            all_permission = {perm.menu_id: perm for perm in permission_list}
            self.cache.set(key, all_permission, timeout)

        if menu_id is not None:
            return all_permission.get(menu_id, {})

        return all_permission
