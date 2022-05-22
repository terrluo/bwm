from attr import validate
from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf, Regexp

from .model import Menu


class AddMenuSchema(Schema):
    menu_name = fields.String(required=True, validate=[Length(min=1)])
    menu_order = fields.Integer(required=True, allow_none=False)
    menu_type = fields.Integer(
        required=True, validate=[OneOf([Menu.MenuType.MENU, Menu.MenuType.BUTTON])]
    )
    parent_id = fields.Integer(load_default=0)
    route_key = fields.String(
        required=True, validate=[Regexp(r".*#(GET|POST|PUT|DELETE)")]
    )
    is_visible = fields.Boolean(required=True, allow_none=False)
