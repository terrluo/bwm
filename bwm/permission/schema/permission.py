from marshmallow import Schema, fields, validates_schema

from bwm.model import menu, permission
from bwm.permission.error.permission import PermissionError
from bwm.util.component import get_db

_db = get_db()


def _validate_menu(menu_id: int):
    if not _db.session.query(menu.Menu.query.filter_by(id=menu_id).exists()).scalar():
        raise PermissionError.MENU_NOT_FOUND


def _validate_role(role_id: int):
    if not _db.session.query(
        permission.Role.query.filter_by(id=role_id).exists()
    ).scalar():
        raise PermissionError.ROLE_NOT_FOUND


class AddPermission(Schema):
    role_id = fields.Int(required=True, validate=[_validate_role])
    menu_id = fields.Int(required=True, validate=[_validate_menu])
    is_visible = fields.Bool(required=True)
    is_operate = fields.Bool(required=True)

    @validates_schema(skip_on_field_errors=True)
    def validate_schema(self, data, **kwargs):
        role_id = data["role_id"]
        menu_id = data["menu_id"]

        if _db.session.query(
            permission.Permission.query.filter_by(
                role_id=role_id, menu_id=menu_id
            ).exists()
        ).scalar():
            raise PermissionError.EXISTED
