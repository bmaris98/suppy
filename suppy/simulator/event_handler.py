from suppy.utils.prio_queue import PrioQueue
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.atomics.calibrated_atomic import CalibratedAtomic
from suppy.simulator.atomics.atomic import Atomic
from suppy.simulator.atomics.atomic_states import AtomicStates
from typing import List, Tuple
from copy import deepcopy

from suppy.utils.borg import Borg
from suppy.models.discrete_event import DiscreteEvent

class EventHandler(Borg):
    _shared_state = {}

    def __init__(self):
        Borg.__init__(self)
        self._time: int = 0
        self._event_queue: PrioQueue = PrioQueue()
        self._log = []

    @property
    def time(self):
        return self._time

    def run_on_network(self, network: AtomicNetwork):
        self._time = 0
        starts = network.start_atomics
        for start in starts:
            start.try_log_ready_state()
        self._run_loop()
        
    def _run_loop(self):
        while self._has_events():
            self._time, event = self._deque_event()
            self._log.append((self._time, event))
            if event.state == AtomicStates.DONE:
                event.atomic.done(event.state)
            if event.state == AtomicStates.CALIBRATION_DONE:
                event.atomic.done(event.state)
            

    def _queue_event(self, time: int, event: DiscreteEvent):
        self._event_queue.queue((time, event))

    def _deque_event(self) -> Tuple[int, DiscreteEvent]:
        return self._event_queue.deque()

    # def _peek_event(self) -> Tuple[int, DiscreteEvent]:
    #     top = self._event_queue.get()
    #     copy = deepcopy(top)
    #     self._event_queue.put(top)
    #     return copy

    def atomic_ready(self, atomic: Atomic) -> None:
        event = DiscreteEvent(AtomicStates.DONE, atomic)
        self._queue_event(self._time + atomic.duration, event)

    def atomic_calibration(self, atomic: CalibratedAtomic) -> None:
        event = DiscreteEvent(AtomicStates.CALIBRATION_DONE, atomic)
        self._queue_event(self._time + atomic.calibration_duration, event)

    def _has_events(self) -> bool:
        return not self._event_queue.empty()