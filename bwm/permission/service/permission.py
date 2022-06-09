import typing as t

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
        p = self.model(
            role_id=data["role_id"],
            menu_id=data["menu_id"],
            is_visible=data["is_visible"],
            is_operate=data["is_operate"],
        )
        self.db.session.add(p)
        self.db.session.commit()
        self._update_permission_cache(p)
        return p

    def get_user_permission_data(self, user_id: int, timeout=60 * 60 * 24):
        user_key = CacheKey.user_permission(user_id)
        user_permission_data: t.Optional[Data] = self.cache.get(user_key)
        if user_permission_data is None:
            from bwm.permission.service.role_user import RoleUserService

            user_permission_data = {}
            role_ids = RoleUserService().get_role_ids(user_id)
            permission_data_list: t.List[Data] = self._get_role_permission_data(
                role_ids, timeout
            ).values()
            for permission_data in permission_data_list:
                for route_key, data in permission_data.items():
                    is_visible = data["is_visible"]
                    is_operate = data["is_operate"]
                    old_data = user_permission_data.setdefault(route_key, data)
                    if is_visible:
                        old_data["is_visible"] = is_visible
                    if is_operate:
                        old_data["is_operate"] = is_operate
            self.cache.set(user_key, user_permission_data, timeout=timeout)
        return user_permission_data

    def _update_permission_cache(self, p: _Permission):
        return

    def _get_role_permission_data(self, role_ids: t.Set[int], timeout: int = None):
        if timeout is None:
            timeout = self.cache_timeout

        role_permission_data = {}
        for role_id in role_ids:
            role_key = CacheKey.role_permission(role_id)
            role_permission = self.cache.get(role_key)
            if role_permission:
                role_permission_data[role_id] = role_permission

        no_cache_role_ids = role_ids - set(role_permission_data.keys())
        no_cache_role_permission_data = self._get_no_cache_role_permission_data(
            no_cache_role_ids
        )
        role_permission_data.update(no_cache_role_permission_data)

        for role_id in no_cache_role_ids:
            role_key = CacheKey.role_permission(role_id)
            self.cache.set(
                role_key, no_cache_role_permission_data[role_id], timeout=timeout
            )
        return role_permission_data

    def _get_no_cache_role_permission_data(self, no_cache_role_ids):
        from bwm.menu.service.menu import MenuService

        menu_service = MenuService()
        no_cache_role_permission_data = {}
        no_cache_role_permission_list = []
        if no_cache_role_ids:
            no_cache_role_permission_list = (
                self.available.filter(
                    self.model.role_id.in_(no_cache_role_ids),
                )
                .with_entities(
                    self.model.role_id,
                    self.model.menu_id,
                    self.model.is_visible,
                    self.model.is_operate,
                )
                .order_by(self.model.role_id, self.model.menu_id)
            ).all()

        for permission_data in no_cache_role_permission_list:
            permission_data: Data = permission_data._asdict()
            role_id = permission_data["role_id"]
            menu_id = permission_data["menu_id"]
            route_key = menu_service.get_route_key(menu_id)
            no_cache_role_permission_data.setdefault(role_id, {})[route_key] = dict(
                is_visible=permission_data["is_visible"],
                is_operate=permission_data["is_operate"],
            )
        return no_cache_role_permission_data
