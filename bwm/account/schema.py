from marshmallow import Schema, fields


class UserSchema(Schema):
    user_id = fields.Integer(required=True, allow_none=False)


class LoginSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)


class RegisterSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)
