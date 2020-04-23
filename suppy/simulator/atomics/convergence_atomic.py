from suppy.utils.stats_constants import CONVERGENCE, TYPE
from typing import Any, Dict
from suppy.simulator.atomics.atomic import Atomic


class ConvergenceAtomic(Atomic):

    def __init__(self, uid: str, seh, name: str):
        Atomic.__init__(self, uid, seh, name, 0, 0)

    def _load_input(self) -> None:
        for input_stream in self._input_streams:
            if input_stream.has_output:
                self._loaded_input.append(input_stream.consume())
                return

    def _has_all_data(self) -> bool:
        for input_stream in self._input_streams:
            if input_stream.has_output:
                return True
        return False

    def _do_process(self) -> None:
        self._output_streams[0].try_load(self._loaded_input[0])

    def get_stats(self) -> Dict[str, Any]:
        stats = Atomic.get_stats(self)
        stats[TYPE] = CONVERGENCE
        return stats