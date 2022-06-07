from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class RoleError:
    """权限错误"""

    EXISTED = Error(code=70000, message=_("角色已存在"))
