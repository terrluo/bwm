from marshmallow import Schema, fields


class LoginSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)
