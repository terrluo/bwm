from gettext import gettext

from flask_restful import Resource as _Resource
from flask_restful import fields, marshal_with

_ = gettext


class Resource(_Resource):
    def success(self, message: str = _("成功")):
        return {"message": message}


common_marshal = marshal_with({"message": fields.String()})
