from bwm.core.error import Error
from flask_babel import lazy_gettext as _


class MenuError:
    """菜单错误"""

    EXISTED = Error(code=40000, message=_("菜单已存在"))
    ROUTE_NOT_FOUND = Error(code=40001, message=_("路由不存在"))