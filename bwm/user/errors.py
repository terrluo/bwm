from flask_babel import lazy_gettext as _

from bwm.core.error import Error


class UserError:
    """用户错误码"""

    NOT_FOUND = Error(code=30000, message=_("用户不存在"))
