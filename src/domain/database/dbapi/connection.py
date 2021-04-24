from abc import ABC, abstractmethod

from domain.database.dbapi.cursor import Cursor


class Connection(ABC):

    def __init__(self):
        pass

    """
    Close the connection now (rather than whenever .__del__() is called).

    The connection will be unusable from this point forward; an Error (or subclass) exception will be raised if any
    operation is attempted with the connection. The same applies to all cursor objects trying to use the connection. 
    Note that closing a connection without committing the changes first will cause an implicit rollback to be performed.
    """
    @abstractmethod
    def close(self):
        raise NotImplementedError

    """
    Commit any pending transaction to the database.

    Note that if the database supports an auto-commit feature, this must be initially off. An interface method may be 
    provided to turn it back on. 

    Database modules that do not support transactions should implement this method with void functionality.
    """
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    """
    This method is optional since not all databases provide transaction support.

    In case a database does provide transactions this method causes the database to roll back to the start of any pending 
    transaction. Closing a connection without committing the changes first will cause an implicit rollback to be performed.
    """
    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    """
    Return a new Cursor Object using the connection.

    If the database does not provide a direct cursor concept, the module will have to emulate cursors using other means 
    to the extent needed by this specification.
    """
    @abstractmethod
    def cursor(self) -> Cursor:
        raise NotImplementedError
