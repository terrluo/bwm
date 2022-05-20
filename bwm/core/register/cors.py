from flask_cors import CORS

from bwm.core.register.base import Component


class CORSComponent(Component):
    def register(self):
        CORS(self._app)
