from bwm.util.component import get_cache, get_db

_cache = get_cache()
_db = get_db()


class Service:
    db = _db

    def page(self, query, page: int, limit: int):
        return query.slice((page - 1) * limit, page * limit)


class CacheService(Service):
    cache = _cache
