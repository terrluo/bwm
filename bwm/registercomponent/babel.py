from flask import g, request
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

        @babel.timezoneselector
        def get_timezone():
            timezone = getattr(g, "timezone", None)
            if timezone is None:
                g.timezone = timezone = self.app.config["LOCAL_TIMEZONE"]
            return timezone
