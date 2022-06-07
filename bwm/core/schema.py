from functools import partial, wraps

from marshmallow import Schema, fields
from marshmallow.validate import Range

from bwm.type import ServiceData


def load_schema(schema: Schema, is_method=True):
    def inner(func):
        def wrapper(self, data: ServiceData, *args, **kwargs):
            load_data = schema.load(data)
            return func(self, load_data, *args, **kwargs)

        if is_method:
            wrapper = wraps(func)(wrapper)
        else:
            wrapper = wraps(func)(partial(wrapper, self=None))
        return wrapper

    return inner


class PageSchema(Schema):
    page = fields.Integer(load_default=1, validate=[Range(min=1)])
    limit = fields.Integer(load_default=10, validate=[Range(min=1)])
