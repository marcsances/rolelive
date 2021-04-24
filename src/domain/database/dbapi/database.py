from abc import ABC, abstractmethod

from domain.database.dbapi.connection import Connection
from domain.database.queryapi.query_set import QuerySet
from domain.guild.database.guild_queries import GuildQueries


class Database(ABC):

    @abstractmethod
    def __init__(self):
        self._conn = None

    @abstractmethod
    def connect(self) -> Connection:
        raise NotImplementedError

    @property
    @abstractmethod
    def connection(self) -> Connection:
        return self._conn

    @abstractmethod
    def get_bootstrap_queries(self) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_guild_queries(self) -> GuildQueries:
        raise NotImplementedError
