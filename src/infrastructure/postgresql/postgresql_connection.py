from psycopg2._psycopg import connection

from domain.database.dbapi.connection import Connection
from infrastructure.postgresql.postgresql_cursor import PostgreSQLCursor


class PostgreSQLConnection(Connection):

    def __init__(self, pg_connection: connection):
        super().__init__()
        self.__pg_connection = pg_connection

    def close(self):
        return self.__pg_connection.close()

    def commit(self):
        return self.__pg_connection.commit()

    def rollback(self):
        return self.__pg_connection.rollback()

    def cursor(self, name=None, cursor_factory=None, scrollable=None, withhold=False) -> PostgreSQLCursor:
        return PostgreSQLCursor(self.__pg_connection.cursor(name, cursor_factory, withhold), self.__pg_connection)
