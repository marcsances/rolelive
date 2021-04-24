from abc import ABC, abstractmethod

from domain.database.queryapi.query import Query


class GuildQueries(ABC):

    """
    INSERT INTO Guild(guildId, guildName) VALUES(%s, %s)
    """
    @abstractmethod
    def create_guild(self, guild_id: int, guild_name: str) -> Query:
        raise NotImplementedError

    """
    SELECT guildId, guildName FROM Guild WHERE guildId=%s
    """
    @abstractmethod
    def get_guild(self, guild_id: int) -> Query:
        raise NotImplementedError

    """
    INSERT INTO GuildPreferences(guildId, prefkey, value) VALUES (%s, %s, %s)
    ON CONFLICT (guildId, prefKey) DO UPDATE SET value = %s
    """
    @abstractmethod
    def set_guild_preference(self, guild_id: int, prefKey: str, prefValue: str) -> Query:
        raise NotImplementedError

    """
    SELECT guildId, prefKey, value FROM guildpreferences WHERE guildid=%s AND prefKey=%s
    """
    @abstractmethod
    def get_guild_preference(self, guild_id: int, prefKey: str) -> Query:
        raise NotImplementedError
