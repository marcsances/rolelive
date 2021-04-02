from typing import Any, Dict, TypeVar, Generic

from domain.base.entity import Entity

T = TypeVar('T')


class Reifiable(Entity, Generic[T]):

    def __init__(self):
        super().__init__()
        self.package: str = ''
        self.module: str = ''
        self.args: Dict[str, Any] = {}
