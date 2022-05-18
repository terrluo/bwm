from gettext import gettext

from bwmv2.core.errors import Error

_ = gettext


class UserError:
    """用户错误码"""

    NOT_FOUND = Error(code=30000, message=_("用户不存在"))
