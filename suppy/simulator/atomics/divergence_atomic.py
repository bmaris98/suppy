from suppy.utils.stats_constants import DIVERGENCE, TYPE
from typing import Any, Dict
from suppy.simulator.atomics.atomic import Atomic


class DivergenceAtomic(Atomic):

    def __init__(self, uid: str, seh, name: str):
        Atomic.__init__(self, uid, seh, name, 0, 0)

    def get_stats(self) -> Dict[str, Any]:
        stats = Atomic.get_stats(self)
        stats[TYPE] = DIVERGENCE
        return stats

    def _all_output_clear(self) -> bool:
        for output_stream in self._output_streams:
            if not output_stream.has_input:
                return True
        return False

    def _do_process(self) -> None:
        resource = self._loaded_input[0]
        for output_stream in self._output_streams:
            if not output_stream.has_input:
                output_stream.try_load(resource)
                return