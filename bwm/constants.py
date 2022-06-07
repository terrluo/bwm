from enum import Enum


class Env(str, Enum):
    DEV = "development"
    PROD = "production"


class CacheKey:
    @classmethod
    def menu(cls):
        return "menu"

    @classmethod
    def permission(cls, role_id: int):
        return f"permission_{role_id}"
