class TimePoint:

    def __init__(self, real_time: int, priority: int):
        self._real_time = real_time
        self._priority = priority

    def __cmp__(self, other):
        if self == other:
            return 0
        if self < other:
            return -1
        return 1

    def __eq__(self, other):
        if not isinstance(other, TimePoint):
            return NotImplemented
        return self.real_time == other.real_time and self.priority == other.priority

    def __lt__(self, other):
        if not isinstance(other, TimePoint):
            return NotImplemented
        if self.real_time == other.real_time:
            return self.priority < other.priority
        return self.real_time < other.real_time

    def __le__(self, other):
        if not isinstance(other, TimePoint):
            return NotImplemented
        if self == other:
            return True
        return self < other

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    @property
    def real_time(self) -> int:
        return self._real_time

    @property
    def priority(self) -> int:
        return self._priority