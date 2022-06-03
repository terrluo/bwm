import sqlalchemy as sa

from bwm.core.model import BaseModel, IsType


class Menu(BaseModel):
    """菜单"""

    __tablename__ = "menu_menu"
    __table_args__ = (sa.UniqueConstraint("parent_id", "menu_type", "menu_name"),)

    class MenuType:
        """菜单类型"""

        MENU = 1
        BUTTON = 2

    class IsVisible(IsType):
        """是否可见"""

    menu_name = sa.Column(sa.String(32), nullable=False, comment="菜单名称")
    menu_order = sa.Column(sa.Integer, nullable=False, default=0, comment="菜单排序(从小到大排)")
    menu_type = sa.Column(
        sa.SmallInteger,
        nullable=False,
        default=MenuType.MENU,
        comment="菜单类型(1:菜单 2:按钮)",
    )
    parent_id = sa.Column(sa.Integer, nullable=False, default=0, comment="父菜单id")
    route_key = sa.Column(
        sa.String(128), nullable=False, default="", comment="路由key,可以通过key获取到对应的路由"
    )
    is_visible = sa.Column(
        sa.Boolean, nullable=False, default=IsVisible.YES, comment="菜单本身是否可见"
    )
