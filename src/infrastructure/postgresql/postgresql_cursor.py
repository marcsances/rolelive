from typing import Sequence, Any, Union, Iterable

from psycopg2._psycopg import cursor

from domain.database.dbapi.connection import Connection
from domain.database.dbapi.cursor import Cursor
from domain.database.dbapi.cursor_description import Column


class PostgreSQLCursor(Cursor):

    def __init__(self, pg_cursor: cursor, pg_connection):
        super().__init__()
        self.__pg_cursor = pg_cursor
        self.__pg_connection = pg_connection

    @property
    def description(self) -> Sequence[Column]:
        return list(map(lambda entry: Column(entry), self.__pg_cursor.description))

    @property
    def rowcount(self) -> int:
        return self.__pg_cursor.rowcount

    def callproc(self, procname: str):
        return self.__pg_cursor.callproc(procname)

    def close(self):
        return self.__pg_cursor.close()

    def execute(self, operation: str, *parameters: Iterable[Any]):
        return self.__pg_cursor.execute(operation, parameters)

    def executemany(self, operation: str, seq_of_parameters: Sequence[Sequence[Any]]):
        return self.__pg_cursor.executemany(operation, seq_of_parameters)

    def fetchone(self) -> Union[Sequence[Any], None]:
        return self.__pg_cursor.fetchone()

    def fetchmany(self, size=None) -> Sequence[Sequence[Any]]:
        if size is None:
            size = self.__pg_cursor.arraysize
        return self.__pg_cursor.fetchmany(size)

    def fetchall(self) -> Sequence[Sequence[Any]]:
        return self.__pg_cursor.fetchall()

    def nextset(self) -> Union[bool, None]:
        return self.__pg_cursor.nextset()

    def setinputsizes(self, sizes: Sequence[Any]):
        return self.__pg_cursor.setinputsizes(sizes)

    def setouputsize(self, size: int, column: int = None):
        return self.__pg_cursor.setoutputsize(size, column)

    def mogrify(self, operation: str, *parameters: Iterable[Any]) -> str:
        return self.__pg_cursor.mogrify(operation, parameters)

    def connection(self) -> Connection:
        return self.__pg_connection
