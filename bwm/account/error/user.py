from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class UserError:
    """用户错误码"""

    NOT_FOUND = Error(code=40000, message=_("用户不存在"))
    PERMISSION_DENIED = Error(code=40001, message=_("没有权限"))
