from abc import ABC, abstractmethod


class Database(ABC):

    @abstractmethod
    def __init__(self):
        pass
