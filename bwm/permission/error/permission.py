from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class PermissionError:
    """权限错误"""

    EXISTED = Error(60000, _("权限已存在"))
    MENU_NOT_FOUND = Error(60001, _("菜单不存在"))
    ROLE_NOT_FOUND = Error(60002, _("角色不存在"))
