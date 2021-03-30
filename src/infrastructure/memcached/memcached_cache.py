from domain.cache.cache import Cache


class MemcachedCache(Cache):
    def __init__(self):
        super().__init__()
