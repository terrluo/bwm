import typing as t

from bwm.core.schema import load_schema
from bwm.core.service import CacheService
from bwm.model import permission
from bwm.permission.schema import AddPermission


class PermissionService(CacheService):
    model = permission.Permission

    @load_schema(AddPermission())
    def add_permission(self, data: t.Dict[str, t.Any]):
        _permission = self.model(
            role_id=data["role_id"],
            menu_id=data["menu_id"],
            is_visible=data["is_visible"],
            is_operate=data["is_operate"],
        )
        self.db.session.add(_permission)
        self.db.session.commit()
        return _permission
