from typing import Union, Sequence, Any

from domain.database.queryapi.query import Query


class FetchQuery(Query):

    def fetchone(self) -> Union[Sequence[Any], None]:
        return self._cursor.fetchone()

    def fetchmany(self, size=None) -> Sequence[Sequence[Any]]:
        return self._cursor.fetchmany(size)

    def fetchall(self) -> Sequence[Sequence[Any]]:
        return self._cursor.fetchall()
