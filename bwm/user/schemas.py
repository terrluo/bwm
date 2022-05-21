from marshmallow import Schema, fields


class UserSchema(Schema):
    user_id = fields.Integer(required=True)
