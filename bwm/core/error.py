import typing as t

from flask_babel import lazy_gettext as _


class Error(Exception):
    """错误"""

    def __init__(self, code: int, message: str, http_status=400, **extra_data) -> None:
        super().__init__()

        self._http_status = http_status
        self.code = code
        self.message = message
        self._error = dict(
            code=code,
            message=message,
        )
        self._error.update(extra_data)

    @classmethod
    def from_error(
        cls,
        error: "Error",
        message: t.Optional[str] = None,
        http_status=400,
        **extra_data
    ) -> "Error":
        if message:
            return cls(
                code=error.code, message=message, http_status=http_status, **extra_data
            )
        return cls(
            code=error.code,
            message=error.message,
            http_status=http_status,
            **extra_data
        )

    @property
    def error(self):
        return self._error

    @property
    def http_status(self):
        return self._http_status


class CommonError:
    """通常错误"""

    REQUEST_DATA_ERROR = Error(code=10000, message=_("请求数据错误"))
