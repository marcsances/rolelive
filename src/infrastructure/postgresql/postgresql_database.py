from domain.database.database import Database


class PostgreSQLDatabase(Database):
    def __init__(self):
        super().__init__()
