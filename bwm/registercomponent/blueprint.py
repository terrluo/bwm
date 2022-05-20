from bwm.registercomponent.base import Component


class BlueprintComponent(Component):
    def register(self):
        from bwm.login.api import login_bp
        from bwm.register.api import register_bp
        from bwm.user.api import user_bp

        self._app.register_blueprint(login_bp)
        self._app.register_blueprint(register_bp)
        self._app.register_blueprint(user_bp)
