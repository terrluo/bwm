from gettext import gettext

from bwm.core.errors import Error

_ = gettext


class LoginError:
    """登入错误"""

    USERNAME_PASSWORD_ERROR = Error(code=20000, message=_("用户名或密码错误"))
