from typing import Any, List, Tuple


class PrioQueue:

    def __init__(self):
        self._items: List[Tuple[int, Any]] = []

    def queue(self, item: Tuple[int, Any]) -> None:
        if len(self._items) == 0:
            self._items.append(item)
            return
        i = 0
        while i < len(self._items):
            if item[0] >= self._items[i][0]:
                self._items.insert(i, item)
                return
            i += 1

        self._items.append(item)

    def deque(self) -> Tuple[int, Any]:
        return self._items.pop()

    def empty(self):
        return len(self._items) == 0