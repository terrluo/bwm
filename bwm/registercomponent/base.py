from flask import Flask


class Component:
    def __init__(self, app: Flask) -> None:
        self._app = app

    def register(self):
        raise NotImplementedError()
