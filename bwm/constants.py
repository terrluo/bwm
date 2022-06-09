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
    def user_permission(cls, user_id: int):
        return f"user_permission_{user_id}"

    @classmethod
    def role_permission(cls, role_id: int):
        return f"role_permission_{role_id}"
