from abc import abstractmethod
from suppy.utils.stats_constants import ACTIVE_TIME, HAS_CALIBRATION, IDLE_TIME, NAME, RUNS, SEMI_FINITE, TOTAL_ACTIVE_COST, UID
from suppy.models.resource import Resource
from suppy.simulator.notification import Notification
from suppy.simulator.atomics.atomic_states import AtomicStates
from suppy.simulator.resource_stream import ResourceStream
from typing import Any, Dict, List


class Atomic:

    def __init__(self, uid: str, seh, name: str, duration: int, cost: int):
        self._input_streams: List[ResourceStream] = []
        self._output_streams: List[ResourceStream] = []
        self._state: AtomicStates = AtomicStates.READY
        self._duration: int = duration
        self._runs: int = 0
        self._name: str = name
        self._uid: str = uid
        self._cost: int = cost
        self._seh = seh
        self._loaded_input: List[Resource] = []
    
    def get_stats(self) -> Dict[str, Any]:
        stats = {}
        stats[NAME] = self._name
        stats[ACTIVE_TIME] = self._duration * self._runs
        stats[HAS_CALIBRATION] = False
        stats[IDLE_TIME] = self._seh.time - (self._duration * self._runs)
        stats[TOTAL_ACTIVE_COST] = self._runs * self._cost
        stats[SEMI_FINITE] = self._get_semi_finite()
        stats[RUNS] = self._runs
        stats[UID] = self._uid
        return stats

    def _get_active_time(self) -> int:
        return self._runs * self._duration

    def _get_semi_finite(self):
        items = []
        for output_stream in self._output_streams:
            if not output_stream.peek_input() == None:
                items.append(output_stream.peek_input())
            if not output_stream.peek_output() == None:
                items.append(output_stream.peek_output())
        return items

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> AtomicStates:
        return self._state
    
    @property
    def duration(self) -> int:
        return self._duration

    @property
    def runs(self) -> int:
        return self._runs

    def register_input_stream(self, stream: ResourceStream) -> None:
        self._input_streams.append(stream)
    
    def register_output_stream(self, stream: ResourceStream) -> None:
        self._output_streams.append(stream)

    def notify(self, stream: ResourceStream, notification: Notification) -> None:
        if notification == Notification.INPUT_STREAM_HAS_INPUT:
            self._handle_input_stream_has_input(stream)
        elif notification == Notification.INPUT_STREAM_TRANSFER_COMPLETE:
            self._handle_stream_transfer_complete(stream)
        elif notification == Notification.OUTPUT_STREAM_TRANSFER_COMPLETE:
            self._handle_stream_transfer_complete(stream)
        elif notification == Notification.OUTPUT_STREAM_CONSUMED:
            self._handle_output_stream_consumed(stream)

    def _handle_input_stream_has_input(self, in_stream: ResourceStream) -> None:
        in_stream.try_transfer()

    def _handle_stream_transfer_complete(self, stream: ResourceStream) -> None:
        self.try_log_ready_state()

    def _handle_output_stream_consumed(self, out_stream: ResourceStream) -> None:
        out_stream.try_transfer()

    def try_log_ready_state(self) -> None:
        if self._can_log_ready_state():
            self._state = AtomicStates.ACTIVE
            self._load_input()
            self._publish_is_ready()

    def _can_log_ready_state(self) -> bool:
        return self._has_all_data() and self._all_output_clear() and self._state == AtomicStates.READY and len(self._loaded_input) == 0

    def _all_output_clear(self) -> bool:
        for output_stream in self._output_streams:
            if output_stream.has_input:
                return False
        return True

    def _publish_is_ready(self) -> None:
        self._runs += 1
        self._seh.atomic_ready(self)

    def _load_input(self) -> None:
        for input_stream in self._input_streams:
            self._loaded_input.append(input_stream.consume())

    def _has_all_data(self) -> bool:
        for input_stream in self._input_streams:
            if not input_stream.has_output:
                return False
        return True

    def _process(self) -> None:
        self._post_process()
        self._do_process()
        self._loaded_input = []
    
    def _post_process(self) -> None:
        return

    def done(self, state: AtomicStates) -> None:
        if state == AtomicStates.DONE:
            self._state = AtomicStates.READY
            self._process()
            self.try_log_ready_state()

    @abstractmethod
    def _do_process(self) -> None:
        pass