from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class RegisterError:
    """注册错误码"""

    REGISTERED = Error(code=30000, message=_("已注册"))
