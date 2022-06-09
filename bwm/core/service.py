from bwm.util.component import get_cache, get_db

_db = get_db()
_cache = get_cache()


class Service:
    db = _db
    model = None

    @property
    def available(self):
        return self.model.query.filter_by(is_delete=False)

    def page(self, query, page: int, limit: int):
        return query.slice((page - 1) * limit, page * limit)


class CacheService(Service):
    cache = _cache
