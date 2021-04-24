from abc import ABC, abstractmethod

from domain.database.dbapi.connection import Connection
from domain.database.queryapi.query_set import QuerySet


class Database(ABC):

    @abstractmethod
    def __init__(self):
        pass

    def connect(self) -> Connection:
        raise NotImplementedError

    @abstractmethod
    def get_bootstrap_queries(self) -> QuerySet:
        raise NotImplementedError
