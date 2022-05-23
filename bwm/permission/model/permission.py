import sqlalchemy as sa

from bwm.core.model import BaseModel, IsType


class Permission(BaseModel):
    """权限"""

    __tablename__ = "permission_permission"

    class IsVisible(IsType):
        """是否可见"""

    class IsOperate(IsType):
        """是否有权限"""

    # menu_menu -> permission_permission
    menu_id = sa.Column(sa.Integer, nullable=False, unique=True, comment="菜单id")
    is_visible = sa.Column(
        sa.Boolean, nullable=False, default=IsVisible.YES, comment="是否有查看权限"
    )
    is_operate = sa.Column(
        sa.Boolean, nullable=False, default=IsOperate.NO, comment="是否有操作权限"
    )
