import os

from bwm.component.base import Component


class ConfigComponent(Component):
    def register(self):
        self._app.config.from_object("config.default")
        self._app.config.from_envvar("BWM_CONFIG_FILE")
        instance_config = os.environ.get("INSTANCE_CONFIG")
        if instance_config:
            self._app.config.from_pyfile(instance_config)
