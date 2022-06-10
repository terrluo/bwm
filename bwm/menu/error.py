from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class MenuError:
    """菜单错误"""

    EXISTED = Error(50000, _("菜单已存在"))
    ROUTE_NOT_FOUND = Error(50001, _("路由不存在"))
