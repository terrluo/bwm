from datetime import datetime

import pytz
from flask import current_app, g


def to_local(dt: datetime):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.utc)
    local_timezone = get_timezone()
    return dt.astimezone(local_timezone)


def to_utc(dt: datetime):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=pytz.utc)
    return dt.astimezone(pytz.utc)


def get_timezone():
    timezone = getattr(g, "timezone", None)
    if timezone is None:
        g.timezone = timezone = current_app.config["LOCAL_TIMEZONE"]
    return timezone
