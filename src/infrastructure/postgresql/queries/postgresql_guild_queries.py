from domain.database.queryapi.query import Query
from domain.guild.database.guild_queries import GuildQueries


class PostgreSQLGuildQueries(GuildQueries):
    def create_guild(self, guild_id: int, guild_name: str) -> Query:
        return Query("INSERT INTO Guild(guildId, guildName) VALUES(%s, %s)", guild_id, guild_name)

    def get_guild(self, guild_id: int) -> Query:
        return Query("SELECT guildId, guildName FROM Guild WHERE guildId=%s", guild_id).fetchone()

    def set_guild_preference(self, guild_id: int, prefKey: str, prefValue: str) -> Query:
        return Query("INSERT INTO GuildPreferences(guildId, prefkey, value) VALUES (%s, %s, %s) " +
                     "ON CONFLICT (guildId, prefKey) DO UPDATE SET value = %s",
                     guild_id, prefKey, prefValue, prefValue)

    def get_guild_preference(self, guild_id: int, prefKey: str) -> Query:
        return Query("SELECT guildId, prefKey, value FROM guildpreferences WHERE guildid=%s AND prefKey=%s",
                          guild_id, prefKey)
