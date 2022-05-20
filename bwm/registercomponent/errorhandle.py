from marshmallow import ValidationError

from bwm.core.errors import ApiError
from bwm.registercomponent.base import Component


class ErrorHandlerComponent(Component):
    def register(self):
        @self._app.errorhandler(ValidationError)
        def handle_validation_error(e: ValidationError):
            for error_msg in e.messages.values():
                return {"message": error_msg[0]}, 400
            return {"message": "未知错误"}, 400

        @self._app.errorhandler(ApiError)
        def handle_api_error(e: ApiError):
            return e.error, e.http_status
