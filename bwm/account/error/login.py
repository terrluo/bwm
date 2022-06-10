from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class LoginError:
    """登入错误"""

    USERNAME_PASSWORD_ERROR = Error(20000, _("用户名或密码错误"), http_status=401)
