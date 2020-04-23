from suppy.utils.stats_constants import BUFFER, CAPACITY, TRANSPORT, TYPE, WAS_FULL
from suppy.simulator.atomics.atomic_states import AtomicStates
from suppy.models.resource import Resource
from typing import Any, Dict, List
from suppy.simulator.atomics.atomic import Atomic


class BufferAtomic(Atomic):

    def __init__(self, uid: str, seh, name: str, capacity: int):
        Atomic.__init__(self, uid, seh, name, 0, 0)
        self._was_full = False
        self._items: List[Resource] = []
        self._capacity = capacity

    def _do_process(self) -> None:
        if len(self._loaded_input) == 0:
            self._try_simple_deque()
        else:
            self._try_queue_deque()

    def _can_log_ready_state(self) -> bool:
        # 1) am input, pot stoca, sunt ready -> pun in loaded -> queue + try deque
        # 2) nu am input, am in stoc, sunt ready, output clean -> deque

        if self._has_all_data() and len(self._items) <= self._capacity and self._all_output_clear() and self._state == AtomicStates.READY:
            return True

        if self._has_all_data() and len(self._items) < self._capacity and self._state == AtomicStates.READY:
            return True # if this happens, execution will contain loaded data
        
        if self._no_input() and len(self._items) > 0 and self._all_output_clear() and self._state == AtomicStates.READY:
            return True # if this happens, execution will NOT contain loaded data

        if self._has_all_data() and len(self._items) == self._capacity and self._state == AtomicStates.READY:
            self._was_full = True
        return False

    def _load_input(self) -> None:
        if self._input_streams[0].has_output:
            self._loaded_input.append(self._input_streams[0].consume())

    def _no_input(self) -> bool:
        return not self._input_streams[0].has_output

    def _try_simple_deque(self):
        resource = self._items.pop()
        output_stream = self._output_streams[0]
        success = output_stream.try_load(resource)
        if not success:
            self._items.append(resource)

    def _try_queue_deque(self):
        resource = self._loaded_input[0]
        self._items.append(resource)
        self._try_simple_deque()

    def get_stats(self) -> Dict[str, Any]:
        stats = Atomic.get_stats(self)
        stats[CAPACITY] = self._capacity
        stats[TYPE] = BUFFER
        stats[WAS_FULL] = self._was_full
        return stats
         