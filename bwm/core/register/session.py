from flask_session import Session

from bwm.core.register.base import Component

session = Session()


class SessionComponent(Component):
    def register(self):
        session.init_app(self._app)
