from bwm.component import bcrypt, cache
from bwm.component.db import db
from bwm.component.jwt import jwt


def get_bcrypt():
    return bcrypt


def get_cache():
    return cache


def get_db():
    return db


def get_jwt():
    return jwt
