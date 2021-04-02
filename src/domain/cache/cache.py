from abc import ABC, abstractmethod
from typing import Any


class Cache(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def put(self, key: str, value: Any):
        raise NotImplementedError()

    @abstractmethod
    def get(self, key: str) -> Any:
        raise NotImplementedError()
