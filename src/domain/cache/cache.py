from abc import ABC, abstractmethod


class Cache(ABC):

    @abstractmethod
    def __init__(self):
        pass
