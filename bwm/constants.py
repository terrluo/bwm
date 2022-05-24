from enum import Enum


class Env(str, Enum):
    DEV = "development"
    PROD = "production"
