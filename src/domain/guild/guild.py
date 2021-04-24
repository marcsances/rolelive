from typing import Optional

import inject

from domain.base.entity import Entity
from domain.database.dbapi.database import Database


class Guild(Entity):
    def __init__(self):
        super().__init__()
        self.guild_id: int = 0
        self.guild_name: str = ''

    @classmethod
    @inject.param("database", Database)
    def get_guild(cls, guild_id: int, database: Database = None) -> Optional['Guild']:
        cursor = database.connection.cursor()
        database.get_guild_queries().get_guild(guild_id).execute(cursor)
        results = cursor.fetchone()
        if not results:
            return None
        results[0]
