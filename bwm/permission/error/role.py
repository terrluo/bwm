from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class RoleError:
    """权限错误"""

    EXISTED = Error(70000, _("角色已存在"))
