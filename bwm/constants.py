from enum import Enum


class Env(str, Enum):
    DEV = "development"
    PROD = "production"


class HttpMethod(str, Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    DELETE = "DELETE"


HTTP_METHOD_LIST = (HttpMethod.GET, HttpMethod.PUT, HttpMethod.POST, HttpMethod.DELETE)


class CacheKey:
    @classmethod
    def menu(cls):
        return "menu"

    @classmethod
    def permission(cls, user_id: int):
        return f"permission_{user_id}"
