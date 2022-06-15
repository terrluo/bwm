from typing import TYPE_CHECKING

from flask_jwt_extended import current_user
from marshmallow import Schema, fields, validates_schema

from bwm.account.error.user import UserError
from bwm.util.component import get_db

if TYPE_CHECKING:
    from bwm.model import account

    _User = account.User


class ChangePasswordSchema(Schema):
    old_password = fields.String(required=True, allow_none=False)
    new_password = fields.String(required=True, allow_none=False)
    new_password_check = fields.String(required=True, allow_none=False)

    @validates_schema(skip_on_field_errors=True)
    def validate_schema(self, data: dict, **kwargs):
        old_password = data["old_password"]
        new_password = data["new_password"]
        new_password_check = data["new_password_check"]
        data["user"] = user = self._get_user(data)

        if not user.check_password(old_password):
            raise UserError.OLD_PASSWORD_ERROR

        if new_password != new_password_check:
            raise UserError.NEW_PASSWORD_ERROR

    def _get_user(self, data: dict) -> "_User":
        raise NotImplementedError()


class ChangeOwnPasswordSchema(ChangePasswordSchema):
    def _get_user(self, data: dict) -> "_User":
        db = get_db()
        return db.session.merge(current_user)
