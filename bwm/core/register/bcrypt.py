from flask_bcrypt import Bcrypt

from bwm.core.register.base import Component

bwm_bcrypt = Bcrypt()


class BcryptComponent(Component):
    def register(self):
        bwm_bcrypt.init_app(self._app)
