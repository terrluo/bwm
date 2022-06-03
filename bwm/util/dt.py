import typing as t
from datetime import datetime

import pytz
from flask import current_app, g

TIMEZONE = t.Union[pytz.BaseTzInfo, pytz.tzinfo.StaticTzInfo, pytz.tzinfo.DstTzInfo]


def to_local(dt: datetime):
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(get_timezone())


def to_utc(dt: datetime):
    if dt.tzinfo is None:
        dt = get_timezone().localize(dt)
    return dt.astimezone(pytz.utc)


def get_timezone() -> TIMEZONE:
    timezone = getattr(g, "timezone", None)
    if timezone is None:
        g.timezone = timezone = current_app.config["LOCAL_TIMEZONE"]
    return timezone
