import random
from suppy.utils.stats_constants import RANDOM_ERROR, TYPE
from typing import Any, Dict
from suppy.simulator.atomics.atomic import Atomic


class RandomErrorAtomic(Atomic):

    def __init__(self, uid: str, seh, name: str, error_type: str, error_rate: float):
        Atomic.__init__(self, uid, seh, name, 0, 0)
        self._error_type: str = error_type
        self._error_rate: float = error_rate

    def _do_process(self) -> None:
        resource = self._loaded_input[0]
        random_number = random.uniform(0, 1)
        if random_number <= self._error_rate:
            resource.add_error(self._error_type)
        self._output_streams[0].try_load(resource)

    def get_stats(self) -> Dict[str, Any]:
        stats = Atomic.get_stats(self)
        stats[TYPE] = RANDOM_ERROR
        return stats