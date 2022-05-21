from marshmallow import ValidationError
from flask_babel import lazy_gettext as _

from bwm.core.error import ApiError
from bwm.registercomponent.base import Component


class ErrorHandlerComponent(Component):
    def register(self):
        @self._app.errorhandler(ValidationError)
        def handle_validation_error(e: ValidationError):
            return {"message": _("请求数据错误"), "data": e.messages}, 400

        @self._app.errorhandler(ApiError)
        def handle_api_error(e: ApiError):
            return e.error, e.http_status
