from copy import deepcopy
from suppy.utils.stats_constants import TRANSPORT, TYPE
from typing import Any, Dict
from suppy.simulator.atomics.atomic import Atomic


class TransportAtomic(Atomic):

    def __init__(self, uid: str, seh, name: str, duration: int, cost: int):
        Atomic.__init__(self, uid, seh, name, duration, cost)

    def _do_process(self) -> None:
        resource = deepcopy(self._loaded_input[0])
        self._output_streams[0].try_load(resource)

    def get_stats(self) -> Dict[str, Any]:
        stats = Atomic.get_stats(self)
        stats[TYPE] = TRANSPORT
        return stats
