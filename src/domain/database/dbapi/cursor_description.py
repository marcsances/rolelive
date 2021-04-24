from typing import Sequence

"""
Use this class to populate a DB API 2.0 standard cursor sequence into a more friendly class.
"""


class Column:

    def __init__(self, seq: Sequence):
        assert len(seq) >= 7, "Cursor description sequence must be at least 7 items long"
        self._name, self._type_code, self._display_size, self._internal_size, self._precision, self._scale, self._null_ok = seq

    @property
    def name(self) -> str:
        return self._name

    @property
    def type_code(self):
        return self._type_code

    @property
    def display_size(self) -> int:
        return self.display_size

    @property
    def internal_size(self) -> int:
        return self._internal_size

    @property
    def precision(self):
        return self._precision

    @property
    def scale(self):
        return self.scale

    @property
    def null_ok(self) -> bool:
        return self._null_ok
