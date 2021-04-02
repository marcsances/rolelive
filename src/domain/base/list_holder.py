from typing import TypeVar, Generic, Callable, Iterable

from domain.base.entity import Entity

T = TypeVar('T', bound=Entity)


class ListHolder(list, Generic[T], Entity):

    def __init__(self, factory: Callable[[], T]):
        list.__init__(self)
        Generic.__init__(self)
        self.__factory = factory

    def deserialize(self, obj: Iterable) -> 'ListHolder[T]':
        self.clear()
        for item in obj:
            self.append(self.__factory().from_dict(item))
        return self

    def from_dict(self, obj) -> 'ListHolder[T]':
        if isinstance(obj, Iterable):
            return self.deserialize(obj)
        else:
            # fallback and do nothing
            return self
