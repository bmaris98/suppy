from suppy.utils.stats_constants import NOT_USED_RESOURCES, RESOURCE_COUNT, RESOURCE_TYPE, START, TYPE
from typing import Any, Dict
from suppy.models.resource import Resource
from suppy.simulator.atomics.atomic import Atomic


class StartAtomic(Atomic):

    def __init__(self, uid: str, seh, name: str, output_type: str, count: int):
        Atomic.__init__(self, uid, seh, name, 0, 0)
        self._output_type: str = output_type
        self._count: int = count
        self._initial_count: int = count

    def _load_input(self) -> None:
        self._count -= 1

    def _has_all_data(self) -> bool:
        return self._count > 0

    def _do_process(self) -> None:
        resource = Resource(self._output_type)
        self._output_streams[0].try_load(resource)

    def get_stats(self) -> Dict[str, Any]:
        stats = Atomic.get_stats(self)
        stats[TYPE] = START
        stats[RESOURCE_COUNT] = self._initial_count
        stats[NOT_USED_RESOURCES] = self._get_not_used()
        stats[RESOURCE_TYPE] = self._output_type
        return stats

    def _get_not_used(self):
        out_stream = self._output_streams[0]
        extra = 0
        if out_stream.has_input:
            extra += 1
        if out_stream.has_output:
            extra += 1
        return self._count + extra
