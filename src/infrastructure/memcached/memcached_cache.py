from typing import Any

from pymemcache import PooledClient

from domain.cache.cache import Cache

import json


class MemcachedCache(Cache):
    def __init__(self, host, port):
        super().__init__()
        self.__memcached = PooledClient(host, port)

    def put(self, key: str, value: Any):
        self.__memcached.set(key, json.dumps(value))

    def get(self, key: str) -> Any:
        return json.loads(self.__memcached.get(key))
