from bwm.util.component import get_cache, get_db

_cache = get_cache()
_db = get_db()


class Service:
    db = _db


class CacheService(Service):
    cache = _cache
