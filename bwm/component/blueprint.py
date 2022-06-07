from bwm.component.base import Component


class BlueprintComponent(Component):
    def register(self):
        from bwm.account.api.login import login_bp
        from bwm.account.api.register import register_bp
        from bwm.account.api.user import user_bp
        from bwm.menu.api import menu_bp
        from bwm.permission.api.role import role_bp

        self._app.register_blueprint(login_bp)
        self._app.register_blueprint(menu_bp)
        self._app.register_blueprint(register_bp)
        self._app.register_blueprint(user_bp)
        self._app.register_blueprint(role_bp)
