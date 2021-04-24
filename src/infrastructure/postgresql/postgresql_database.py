import psycopg2

from domain.database.dbapi.database import Database
from domain.database.queryapi.query_set import QuerySet
from infrastructure.postgresql.postgresql_connection import PostgreSQLConnection
from infrastructure.postgresql.queries.postgresql_boostrap_queries import PostgreSQLBootstrapQueries


class PostgreSQLDatabase(Database):
    def __init__(self, host="localhost", port=5432, dbname="rolelive", username="rolelive", password="rolelive"):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__dbname = dbname
        self.__username = username
        self.__password = password

    def connect(self) -> PostgreSQLConnection:
        pgconn = psycopg2.connect(host=self.__host, port=self.__port, dbname=self.__dbname, user=self.__username,
                                  password=self.__password)
        return PostgreSQLConnection(pgconn)

    def get_bootstrap_queries(self) -> QuerySet:
        return PostgreSQLBootstrapQueries()
