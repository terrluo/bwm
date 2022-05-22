from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class LoginError:
    """登入错误"""

    USERNAME_PASSWORD_ERROR = Error(code=20000, message=_("用户名或密码错误"), http_status=401)


class RegisterError:
    """注册错误码"""

    REGISTERED = Error(code=30000, message=_("已注册"))


class UserError:
    """用户错误码"""

    NOT_FOUND = Error(code=40000, message=_("用户不存在"))
