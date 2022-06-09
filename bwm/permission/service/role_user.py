import typing as t

from bwm.core.service import Service
from bwm.model import account, permission

_User = account.User
_Role = permission.Role
_RoleUser = permission.RoleUser


class RoleUserService(Service):
    model = _RoleUser

    def get_role_list(self, user_id: t.Union[int, t.Set[int]]):
        role_list = _Role.query.join(
            self.model,
            self.model.role_id == _Role.id,
        )
        if isinstance(user_id, int):
            role_list = role_list.filter(
                self.model.user_id == user_id,
            )
        else:
            role_list = role_list.filter(
                self.model.user_id.in_(user_id),
            )
        return role_list

    def get_role_ids(self, user_id: t.Union[int, t.Set[int]]) -> t.Set[int]:
        role_list = (
            self.get_role_list(user_id)
            .with_entities(
                _Role.id,
            )
            .group_by(_Role.id)
            .all()
        )
        role_ids = {role.id for role in role_list}
        return role_ids

    def get_user_list(self, role_id: t.Union[int, t.Set[int]]):
        role_list = _User.query.join(
            self.model,
            self.model.user_id == _User.id,
        )
        if isinstance(role_id, int):
            role_list = role_list.filter(
                self.model.role_id == role_id,
            )
        else:
            role_list = role_list.filter(
                self.model.role_id.in_(role_id),
            )
        return role_list

    def get_user_ids(self, role_id: t.Set[int]):
        user_list = (
            self.get_user_list(role_id)
            .with_entities(
                _User.id,
            )
            .group_by(_User.id)
            .all()
        )
        user_ids = {user.id for user in user_list}
        return user_ids
