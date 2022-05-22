from bwm.component import cache, db


class Service:
    db = db


class CacheService(Service):
    cache = cache
