import sqlalchemy as sa

from bwm.core.model import BaseModel


class Permission(BaseModel):
    """权限"""

    __tablename__ = "permission_permission"

    # permission_role -> permission_permission
    role_id = sa.Column(sa.Integer, nullable=False, index=True, comment="角色id")
    # menu_menu -> permission_permission
    menu_id = sa.Column(sa.Integer, nullable=False, index=True, comment="菜单id")
    is_visible = sa.Column(sa.Boolean, nullable=False, default=True, comment="是否有查看权限")
    is_operate = sa.Column(sa.Boolean, nullable=False, default=False, comment="是否有操作权限")
