from marshmallow import Schema, fields, validates_schema

from bwm.model import permission
from bwm.permission.error.role import RoleError
from bwm.util.component import get_db


class AddRole(Schema):
    role_name = fields.Str(required=True)

    @validates_schema(skip_on_field_errors=True)
    def validate_schema(self, data, **kwargs):
        role_name = data["role_name"]

        if (
            get_db()
            .session.query(
                permission.Role.query.filter_by(role_name=role_name).exists()
            )
            .scalar()
        ):
            raise RoleError.EXISTED
