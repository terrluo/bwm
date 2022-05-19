from gettext import gettext

from bwm.core.errors import Error

_ = gettext


class RegisterError:
    """注册错误码"""

    REGISTERED = Error(code=10000, message=_("已注册"))
