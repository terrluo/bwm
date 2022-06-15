from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class UserError:
    """用户错误码"""

    NOT_FOUND = Error(40000, _("用户不存在"))
    PERMISSION_DENIED = Error(40001, _("没有权限"))
    OLD_PASSWORD_ERROR = Error(40002, _("旧密码错误"))
    NEW_PASSWORD_ERROR = Error(40003, _("新密码不一致"))
