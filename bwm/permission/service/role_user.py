import typing as t

from bwm.core.service import Service
from bwm.model import permission

_Role = permission.Role
_RoleUser = permission.RoleUser


class RoleUserService(Service):
    model = _RoleUser

    def get_role_list(self, user_id: int):
        role_list = _Role.query.join(
            self.model,
            self.model.role_id == _Role.id,
        ).filter(
            self.model.user_id == user_id,
        )
        return role_list

    def get_role_ids(self, user_id: int) -> t.Set[int]:
        role_list = (
            self.get_role_list(user_id)
            .with_entities(
                _Role.id,
            )
            .all()
        )
        role_ids = {role.id for role in role_list}
        return role_ids
