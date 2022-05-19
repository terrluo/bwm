from marshmallow import Schema, fields


class RegisterSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
