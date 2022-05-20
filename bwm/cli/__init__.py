from flask import Flask

from .translate import register_translate


def register_cli(app: Flask):
    register_translate(app)
