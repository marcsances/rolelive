from abc import ABC, abstractmethod
from asyncio import Future


class Watchdog(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def start(self) -> Future:
        raise NotImplementedError
