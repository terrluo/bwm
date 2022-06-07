from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class PermissionError:
    """权限错误"""

    EXISTED = Error(code=60000, message=_("权限已存在"))
    MENU_NOT_FOUND = Error(code=60001, message=_("菜单不存在"))
