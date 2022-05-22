from flask_babel import lazy_gettext as _
from marshmallow import ValidationError

from bwm.component.base import Component
from bwm.core.error import CommonError, Error


class ErrorHandlerComponent(Component):
    def register(self):
        @self._app.errorhandler(ValidationError)
        def handle_validation_error(e: ValidationError):
            error = Error.from_error(CommonError.REQUEST_DATA_ERROR, data=e.messages)
            return error.error, error.http_status

        @self._app.errorhandler(Error)
        def handle_error(e: Error):
            return e.error, e.http_status
