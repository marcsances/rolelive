from typing import Any, Iterable

import psycopg2

from domain.database.dbapi.cursor import Cursor


class Query:

    def __init__(self, query: str, *params: Iterable[Any]):
        self._query = query
        self._params = params

    def execute(self, cursor: Cursor):
        try:
            cursor.execute(self._query, self._params)
        except psycopg2.Error as e:
            print("Error while running a database query")
            print(e.pgcode)
            print(e.pgerror)
        except Exception as e:
            print("Error while running a database query")
            print(e)
