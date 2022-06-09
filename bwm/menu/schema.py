from marshmallow import Schema, fields, validates_schema
from marshmallow.validate import Length, OneOf, Regexp

from bwm.menu.error import MenuError
from bwm.model import menu
from bwm.util.component import get_db
from bwm.util.permission import check_route_key


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

        if not route_key:
            try:
                check_route_key(route_key)
            except KeyError:
                raise MenuError.ROUTE_NOT_FOUND

        # 检查菜单是否存在
        if (
            get_db()
            .session.query(
                menu.Menu.query.filter_by(
                    parent_id=parent_id, menu_type=menu_type, menu_name=menu_name
                ).exists()
            )
            .scalar()
        ):
            raise MenuError.EXISTED
