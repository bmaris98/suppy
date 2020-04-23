from suppy.utils.stats_constants import NON_REPAIRS, REPAIR, REPAIRS, TYPE
from typing import Any, Dict
from suppy.simulator.atomics.calibrated_atomic import CalibratedAtomic


class RepairAtomic(CalibratedAtomic):

    def __init__(self, uid: str, seh, name: str, duration: int, cost: int, calibration_duration: int, calibration_steps: int, calibration_cost: int, error_type: str):
        CalibratedAtomic.__init__(self, uid, seh, name, duration, cost, calibration_duration, calibration_steps, calibration_cost)
        self._error_type = error_type
        self._non_repairs = 0
        self._actual_repairs = 0

    def _do_process(self) -> None:
        resource = self._loaded_input[0]
        if resource.has_error(self._error_type):
            resource.remove_error(self._error_type)
            self._actual_repairs += 1
        else:
            self._non_repairs += 1
        self._output_streams[0].try_load(resource)

    def get_stats(self) -> Dict[str, Any]:
        stats = CalibratedAtomic.get_stats(self)
        stats[REPAIRS] = self._actual_repairs
        stats[NON_REPAIRS] = self._non_repairs
        stats[TYPE] = REPAIR
        return stats