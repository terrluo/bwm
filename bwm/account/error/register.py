from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class RegisterError:
    """注册错误码"""

    REGISTERED = Error(30000, _("已注册"))
