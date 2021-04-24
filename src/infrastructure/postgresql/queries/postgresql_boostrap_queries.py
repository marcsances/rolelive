from domain.database.queryapi.query import Query
from domain.database.queryapi.query_set import QuerySet


class PostgreSQLBootstrapQueries(QuerySet):

    def __init__(self):
        super().__init__([])
        queries = [
            """
            CREATE TABLE IF NOT EXISTS Guild(
                guildId INT PRIMARY KEY,
                guildName TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Role(
                guildId INT NOT NULL,
                roleId INT NOT NULL,
                adminRole BOOLEAN NOT NULL,
                roleName TEXT,
                PRIMARY KEY (guildId, roleId)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS UserRoles(
                guildId INT NOT NULL,
                userId INT NOT NULL,
                roleId INT NOT NULL,
                FOREIGN KEY (guildId) REFERENCES Guild(guildId),
                FOREIGN KEY (guildId, roleId) REFERENCES Role(guildId, roleId),
                PRIMARY KEY (guildId, userId, roleId)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Stream(
                platformId INT NOT NULL,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                PRIMARY KEY (platformId, name)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS StreamRecord(
                guildId INT NOT NULL,
                platformId INT NOT NULL,
                name TEXT NOT NULL,
                createdBy INT NOT NULL,
                FOREIGN KEY (guildId) REFERENCES Guild(guildId),
                FOREIGN KEY (platformId, name) REFERENCES Stream(platformId, name),
                PRIMARY KEY (guildId, platformId, name, createdBy)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS GuildPreferences(
                guildId INT NOT NULL,
                prefKey TEXT NOT NULL,
                value TEXT NOT NULL,
                FOREIGN KEY (guildId) REFERENCES Guild(guildId),
                PRIMARY KEY (guildId, prefKey)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS NotificationStyle(
                guildId INT NOT NULL,
                channelId INT NOT NULL,
                message TEXT NOT NULL,
                FOREIGN KEY (guildId) REFERENCES Guild(guildId),
                PRIMARY KEY (guildId, channelId)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS StreamFilters(
                guildId INT NOT NULL,
                filterId SERIAL,
                categoryMatch TEXT,
                titleMatch TEXT,
                FOREIGN KEY (guildId) REFERENCES Guild(guildId),
                PRIMARY KEY (guildId, filterId)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS NotifiedChannels(
                guildId INT NOT NULL,
                filterId INT NOT NULL,
                channelId INT NOT NULL,
                FOREIGN KEY (guildId, filterId) REFERENCES StreamFilters(guildId, filterId),
                PRIMARY KEY (guildId, filterId, channelId)
            );
            """
        ]
        self._queries = list(map(lambda query: Query(query), queries))
