from flask import request
from flask_babel import Babel

from bwm.registercomponent.base import Component

babel = Babel()


class BabelComponent(Component):
    def register(self):
        babel.init_app(self._app)

        @babel.localeselector
        def get_locale():
            languages: list = self._app.config.get("LANGUAGES")
            return request.accept_languages.best_match(languages)
