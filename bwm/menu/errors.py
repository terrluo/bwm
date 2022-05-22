from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class MenuError:
    """菜单错误"""

    EXISTED = Error(code=50000, message=_("菜单已存在"))
    ROUTE_NOT_FOUND = Error(code=50001, message=_("路由不存在"))
