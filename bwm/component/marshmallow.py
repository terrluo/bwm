from flask_babel import lazy_gettext as _
from marshmallow import fields

from bwm.component.base import Component


class MarshmallowComponent(Component):
    def register(self):
        fields.Field.default_error_messages = {
            "required": _("参数缺失"),
            "null": _("不能为空"),
            "validator_failed": _("数据错误"),
        }
