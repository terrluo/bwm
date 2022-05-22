import typing as t
from functools import partial, wraps

from marshmallow import Schema


def load_data(schema: Schema, is_method=True):
    def inner(func):
        def wrapper(self, data: t.Dict[str, t.Any], *args, **kwargs):
            load_data = schema.load(data)
            return func(self, load_data, *args, **kwargs)

        if is_method:
            wrapper = wraps(func)(wrapper)
        else:
            wrapper = wraps(func)(partial(wrapper, self=None))
        return wrapper

    return inner
