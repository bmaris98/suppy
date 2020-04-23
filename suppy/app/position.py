from typing import Tuple


class Position:

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def value(self) -> Tuple[int, int]:
        return self._x, self._y

    def add_vector(self, i: int, j: int) -> 'Position':
        return Position(self._x + i, self._y + j)