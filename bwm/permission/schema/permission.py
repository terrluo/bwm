from marshmallow import Schema, fields, validates_schema

from bwm.model import menu, permission
from bwm.permission.error.permission import PermissionError
from bwm.util.component import get_db


class AddPermission(Schema):
    role_id = fields.Int(required=True)
    menu_id = fields.Int(required=True)
    is_visible = fields.Bool(required=True)
    is_operate = fields.Bool(required=True)

    @validates_schema(skip_on_field_errors=True)
    def validate_schema(self, data, **kwargs):
        role_id = data["role_id"]
        menu_id = data["menu_id"]

        db = get_db()

        if not db.session.query(
            menu.Role.query.filter_by(id=role_id).exists()
        ).scalar():
            raise PermissionError.ROLE_NOT_FOUND

        if not db.session.query(
            menu.Menu.query.filter_by(id=menu_id).exists()
        ).scalar():
            raise PermissionError.MENU_NOT_FOUND

        if db.session.query(
            permission.Permission.query.filter_by(
                role_id=role_id, menu_id=menu_id
            ).exists()
        ).scalar():
            raise PermissionError.EXISTED
