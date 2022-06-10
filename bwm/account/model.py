import typing as t

import sqlalchemy as sa
from flask_bcrypt import Bcrypt

from bwm.account.error.user import UserError
from bwm.constants import HTTP_METHOD_LIST, HttpMethod
from bwm.core.model import BaseModel
from bwm.type import Data
from bwm.util.component import get_bcrypt
from bwm.util.model import generate_union_id
from bwm.util.permission import generate_route_key


class User(BaseModel):
    """
    用户

    备注：
        更新密码后需要重新生成 union_id
    """

    __tablename__ = "account_user"

    union_id = sa.Column(
        sa.String(36),
        nullable=False,
        unique=True,
        default=generate_union_id,
        comment="关联id",
    )
    nickname = sa.Column(sa.String(16), nullable=False, unique=True, comment="昵称")
    username = sa.Column(sa.String(16), nullable=False, unique=True, comment="用户名")
    password = sa.Column(sa.String(60), nullable=False, comment="密码")
    is_admin = sa.Column(
        sa.Boolean, nullable=False, default=False, comment="是否是管理员, 管理员有所有权限"
    )

    def check_permission(self, endpoint: str, method: str):
        if not self.has_permission(endpoint, method):
            raise UserError.PERMISSION_DENIED

    def has_permission(self, endpoint: str, method: str) -> bool:
        if self.is_admin:
            return True

        method = method.upper()
        if method not in HTTP_METHOD_LIST:
            return True

        from bwm.permission.service.permission import PermissionService

        permission_data = PermissionService().get_user_permission_data(self.id)
        route_key = generate_route_key(endpoint, method)
        perm: Data = permission_data.get(route_key, {})
        if method == HttpMethod.GET:
            return perm.get("is_visible")
        return perm.get("is_operate")

    def generate_password(
        self, password: str, rounds=None, prefix=None, bcrypt: t.Optional[Bcrypt] = None
    ):
        return (
            self._get_bcrypt(bcrypt)
            .generate_password_hash(password, rounds=rounds, prefix=prefix)
            .decode("utf-8")
        )

    def check_password(self, password: str, bcrypt: t.Optional[Bcrypt] = None):
        return self._get_bcrypt(bcrypt).check_password_hash(self.password, password)

    def _get_bcrypt(self, bcrypt: t.Optional[Bcrypt] = None):
        return bcrypt if bcrypt else get_bcrypt()
