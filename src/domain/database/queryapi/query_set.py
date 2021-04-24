from typing import Iterable

from domain.database.dbapi.cursor import Cursor
from domain.database.queryapi.query import Query


class QuerySet:

    def __init__(self, queries: Iterable[Query]):
        self._queries = queries

    def execute(self, cursor: Cursor):
        for query in self._queries:
            query.execute(cursor)
