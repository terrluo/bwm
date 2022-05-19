import typing as t


class Error:
    """错误"""

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class ApiError(Exception):
    def __init__(self, ret: int, message: str, http_status=400, **extra_data) -> None:
        super().__init__()

        self._http_status = http_status
        self._error = dict(
            ret=ret,
            message=message,
        )
        self._error.update(extra_data)

    @classmethod
    def from_error(
        cls,
        error: Error,
        message: t.Optional[str] = None,
        http_status=400,
        **extra_data
    ) -> "ApiError":
        if message:
            return cls(
                ret=error.code, message=message, http_status=http_status, **extra_data
            )
        return cls(
            ret=error.code, message=error.message, http_status=http_status, **extra_data
        )

    @property
    def error(self):
        return self._error

    @property
    def http_status(self):
        return self._http_status
