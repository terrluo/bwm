from flask import current_app
from marshmallow import Schema, fields, validates_schema
from marshmallow.validate import Length, OneOf, Regexp

from bwm.menu.error import MenuError
from bwm.model import menu
from bwm.util.component import get_db


class AddMenuSchema(Schema):
    menu_name = fields.String(required=True, validate=[Length(min=1)])
    menu_order = fields.Integer(required=True, allow_none=False)
    menu_type = fields.Integer(
        required=True,
        validate=[OneOf([menu.Menu.MenuType.MENU, menu.Menu.MenuType.BUTTON])],
    )
    parent_id = fields.Integer(load_default=0)
    route_key = fields.String(
        load_default="", validate=[Regexp(r".*#(GET|POST|PUT|DELETE)")]
    )
    is_visible = fields.Boolean(required=True, allow_none=False)

    @validates_schema(skip_on_field_errors=True)
    def validate_schema(self, data, **kwargs):
        parent_id = data["parent_id"]
        menu_type = data["menu_type"]
        menu_name = data["menu_name"]
        route_key = data["route_key"]

        self._check_route_key(route_key)

        # 检查菜单是否存在
        is_exist = (
            get_db()
            .session.query(
                menu.Menu.query.filter_by(
                    parent_id=parent_id, menu_type=menu_type, menu_name=menu_name
                ).exists()
            )
            .scalar()
        )
        if is_exist:
            raise MenuError.EXISTED

    def _check_route_key(self, route_key: str):
        if not route_key:
            return

        # 检查路由是否存在
        endpoint, method = self._unpack_route_key(route_key)
        try:
            rules = current_app.url_map.iter_rules(endpoint.lower())
            for rule in rules:
                if method.upper() not in rule.methods:
                    raise KeyError
                break
        except KeyError:
            raise MenuError.ROUTE_NOT_FOUND

    def _unpack_route_key(self, route_key: str):
        endpoint, method = route_key.split("#", 2)
        return endpoint, method
