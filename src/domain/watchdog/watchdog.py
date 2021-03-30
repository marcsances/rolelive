from abc import ABC, abstractmethod


class Watchdog(ABC):

    @abstractmethod
    def __init__(self):
        pass
