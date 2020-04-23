import math
from typing import Any, Dict
from suppy.utils.stats_constants import CALIBRATION_COUNT, CALIBRATION_LEFT, CALIBRATION_TIME, HAS_CALIBRATION, IDLE_TIME, TOTAL_CALIBRATION_COST
from suppy.simulator.atomics.atomic_states import AtomicStates
from suppy.simulator.atomics.atomic import Atomic

class CalibratedAtomic(Atomic):

    def __init__(self, uid: str, seh, name: str, duration: int, cost: int, calibration_duration: int, calibration_steps: int, calibration_cost: int):
        Atomic.__init__(self, uid, seh, name, duration, cost)
        self._calibration_duration: int = calibration_duration
        self._calibration_steps: int = calibration_steps
        self._steps_from_last_calibration: int = 0
        self._calibration_cost = calibration_cost

    @property
    def calibration_duration(self) -> int:
        return self._calibration_duration

    def _post_process(self) -> None:
        self._steps_from_last_calibration += 1
        if self._steps_from_last_calibration == self._calibration_steps:
            self._state = AtomicStates.CALIBRATION
            self._seh.atomic_calibration(self)

    def done(self, state: AtomicStates) -> None:
        Atomic.done(self, state)
        if state == AtomicStates.CALIBRATION_DONE:
            self._steps_from_last_calibration = 0
            self._state = AtomicStates.READY
            self.try_log_ready_state()

    def _get_calibration_count(self) -> int:
        return math.floor(self._runs / self._calibration_steps)

    def _get_calibration_time(self) -> int:
        return self._get_calibration_count() * self._calibration_duration

    def get_stats(self) -> Dict[str, Any]:
        stats = Atomic.get_stats(self)
        stats[HAS_CALIBRATION] = True
        stats[IDLE_TIME] = self._seh.time - self._get_active_time() - self._get_calibration_time()
        stats[TOTAL_CALIBRATION_COST] = self._get_calibration_count() * self._calibration_cost
        stats[CALIBRATION_COUNT] = self._get_calibration_count()
        stats[CALIBRATION_LEFT] = self._calibration_steps - self._steps_from_last_calibration
        stats[CALIBRATION_TIME] = self._get_calibration_time()
        return stats
