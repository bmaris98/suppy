from suppy.utils.stats_constants import TEST, TYPE, WITHOUT_ERROR_COUNT, WITH_ERROR_COUNT
from typing import Any, Dict
from suppy.simulator.atomics.calibrated_atomic import CalibratedAtomic

class VerificationAtomic(CalibratedAtomic):

    def __init__(self, uid: str, seh, name: str, duration: int, cost: int, calibration_duration: int, calibration_steps: int, calibration_cost: int, error_type: str):
        CalibratedAtomic.__init__(self, uid, seh, name, duration, cost, calibration_duration, calibration_steps, calibration_cost)
        self._with_error = 0
        self._without_error = 0
        self._error_type = error_type
    
    def get_stats(self) -> Dict[str, Any]:
        stats = CalibratedAtomic.get_stats(self)
        stats[TYPE] = TEST
        stats[WITH_ERROR_COUNT] = self._with_error
        stats[WITHOUT_ERROR_COUNT] = self._without_error
        return stats

    def _do_process(self) -> None:
        resource = self._loaded_input[0]
        has_error_stream = self._output_streams[0]
        ok_stream = self._output_streams[1]
        if resource.has_error(self._error_type):
            has_error_stream.try_load(resource)
            self._with_error += 1
        else:
            ok_stream.try_load(resource)
            self._without_error += 1
