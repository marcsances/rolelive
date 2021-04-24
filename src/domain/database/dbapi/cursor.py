from abc import ABC, abstractmethod
from typing import Any, Iterable, Union, Sequence

from domain.database.dbapi.cursor_description import Column

"""
Interface largely based and wrapping around Python DB API 2.0 (PEP 249).

These objects represent a database cursor, which is used to manage the context of a fetch operation. Cursors created 
from the same connection are not isolated, i.e., any changes done to the database by a cursor are immediately visible 
by the other cursors. Cursors created from different connections can or can not be isolated, depending on how the 
transaction support is implemented (see also the connection's .rollback() and .commit() methods). 
"""


class Cursor(ABC):

    @abstractmethod
    def __init__(self):
        self._arraysize = 1
        self._closed = False

    """
    This read-only attribute is a sequence of CursorDescription instances.
    """
    @property
    @abstractmethod
    def description(self) -> Sequence[Column]:
        raise NotImplementedError

    """
    This read-only attribute specifies the number of rows that the last .execute*() produced (for DQL statements 
    like SELECT) or affected (for DML statements like UPDATE or INSERT).
    """
    @property
    @abstractmethod
    def rowcount(self) -> int:
        raise NotImplementedError

    """
    (This method is optional since not all databases provide stored procedures.)
    
    Call a stored database procedure with the given name. The sequence of parameters must contain one entry for each 
    argument that the procedure expects. The result of the call is returned as modified copy of the input sequence. Input 
    parameters are left untouched, output and input/output parameters replaced with possibly new values. 
    
    The procedure may also provide a result set as output. This must then be made available through the standard .fetch*(
    ) methods.
    
    :raises NotImplementedError: if method not supported by DBMS
    """
    @abstractmethod
    def callproc(self, procname: str):
        raise NotImplementedError

    """
    Close the cursor now (rather than whenever __del__ is called).

    The cursor will be unusable from this point forward; an Error (or subclass) exception will be raised if any 
    operation is attempted with the cursor. 
    """
    @abstractmethod
    def close(self):
        self._closed = True

    """
    Prepare and execute a database operation (query or command).

    Parameters may be provided as sequence or mapping and will be bound to variables in the operation. Variables are 
    specified in a database-specific notation (see the module's paramstyle attribute for details). 
    
    A reference to the operation will be retained by the cursor. If the same operation object is passed in again, 
    then the cursor can optimize its behavior. This is most effective for algorithms where the same operation is used, 
    but different parameters are bound to it (many times). 
    
    For maximum efficiency when reusing an operation, it is best to use the .setinputsizes() method to specify the 
    parameter types and sizes ahead of time. It is legal for a parameter to not match the predefined information; the 
    implementation should compensate, possibly with a loss of efficiency. 
    
    The parameters may also be specified as list of tuples to e.g. insert multiple rows in a single operation, 
    but this kind of usage is deprecated: .executemany() should be used instead. 
    
    Return values are not defined.
    """
    @abstractmethod
    def execute(self, operation: str, *parameters: Iterable[Any]):
        raise NotImplementedError

    """
    Prepare a database operation (query or command) and then execute it against all parameter sequences or 
    mappings found in the sequence seq_of_parameters. 

    Modules are free to implement this method using multiple calls to the .execute() method or by using array 
    operations to have the database process the sequence as a whole in one call. 
    
    Use of this method for an operation which produces one or more result sets constitutes undefined behavior, 
    and the implementation is permitted (but not required) to raise an exception when it detects that a result set 
    has been created by an invocation of the operation. 
    
    The same comments as for .execute() also apply accordingly to this method.
    
    Return values are not defined.
    """
    @abstractmethod
    def executemany(self, operation: str, seq_of_parameters: Sequence[Sequence[Any]]):
        raise NotImplementedError

    """
    Fetch the next row of a query result set, returning a single sequence, or None when no more data is available.

    An Error (or subclass) exception is raised if the previous call to .execute*() did not produce any result set or 
    no call was issued yet.
    """
    @abstractmethod
    def fetchone(self) -> Union[Sequence[Any], None]:
        raise NotImplementedError

    """
    Fetch the next set of rows of a query result, returning a sequence of sequences (e.g. a list of tuples). An 
    empty sequence is returned when no more rows are available. 

    The number of rows to fetch per call is specified by the parameter. If it is not given, the cursor's arraysize 
    determines the number of rows to be fetched. The method should try to fetch as many rows as indicated by the size 
    parameter. If this is not possible due to the specified number of rows not being available, fewer rows may be returned. 
    
    An Error (or subclass) exception is raised if the previous call to .execute*() did not produce any result set or no 
    call was issued yet. 
    
    Note there are performance considerations involved with the size parameter. For optimal performance, it is usually 
    best to use the .arraysize attribute. If the size parameter is used, then it is best for it to retain the same value 
    from one .fetchmany() call to the next.
    """
    @abstractmethod
    def fetchmany(self, size=None) -> Sequence[Sequence[Any]]:
        raise NotImplementedError

    """
    Fetch all (remaining) rows of a query result, returning them as a sequence of sequences (e.g. a list of tuples). 
    Note that the cursor's arraysize attribute can affect the performance of this operation.

    An Error (or subclass) exception is raised if the previous call to .execute*() did not produce any result set or no 
    call was issued yet.
    """
    @abstractmethod
    def fetchall(self) -> Sequence[Sequence[Any]]:
        raise NotImplementedError

    """
    (This method is optional since not all databases support multiple result sets.)

    This method will make the cursor skip to the next available set, discarding any remaining rows from the current set.
    
    If there are no more sets, the method returns None. Otherwise, it returns a true value and subsequent calls to the 
    .fetch*() methods will return rows from the next result set.
    
    An Error (or subclass) exception is raised if the previous call to .execute*() did not produce any result set or no 
    call was issued yet.
    """
    @abstractmethod
    def nextset(self) -> Union[bool, None]:
        raise NotImplementedError

    """
    This read/write attribute specifies the number of rows to fetch at a time with .fetchmany(). It defaults to 1 
    meaning to fetch a single row at a time. 

    Implementations must observe this value with respect to the .fetchmany() method, but are free to interact with the 
    database a single row at a time. It may also be used in the implementation of .executemany().
    """
    @property
    def arraysize(self) -> int:
        return self._arraysize

    @arraysize.setter
    def arraysize(self, value: int):
        self._arraysize = value

    """
    This can be used before a call to .execute*() to predefine memory areas for the operation's parameters.

    sizes is specified as a sequence — one item for each input parameter. The item should be a Type Object that 
    corresponds to the input that will be used, or it should be an integer specifying the maximum length of a string 
    parameter. If the item is None, then no predefined memory area will be reserved for that column (this is useful 
    to avoid predefined areas for large inputs). 
    
    This method would be used before the .execute*() method is invoked.
    
    Implementations are free to have this method do nothing and users are free to not use it.
    """
    @abstractmethod
    def setinputsizes(self, sizes: Sequence[Any]):
        pass

    """
    Set a column buffer size for fetches of large columns (e.g. LONGs, BLOBs, etc.). The column is specified as an 
    index into the result sequence. Not specifying the column will set the default size for all large columns in the 
    cursor. 

    This method would be used before the .execute*() method is invoked.
    
    Implementations are free to have this method do nothing and users are free to not use it.
    """
    @abstractmethod
    def setouputsize(self, size: int, column: int = None):
        pass

    """
    (Optional DB API extension)
    
    Return a query string after arguments binding. The string returned is exactly the one that would be sent to the 
    database running the execute() method or similar.

    The returned string is always a bytes string.
    """
    def mogrify(self, operation: str, *parameters: Iterable[Any]) -> str:
        raise NotImplementedError

    """
    (Optional DB API extension)
    
    Read-only boolean attribute: specifies if the cursor is closed (True) or not (False).
    """
    def closed(self) -> bool:
        return self._closed

    def connection(self):
        raise NotImplementedError
