from suppy.utils.stats_constants import ERRORS_FOUND, ERRORS_MISSED, TEST, TYPE, WITHOUT_ERROR_COUNT, WITH_ERROR_COUNT
from typing import Any, Dict
from suppy.simulator.atomics.calibrated_atomic import CalibratedAtomic

class VerificationAtomic(CalibratedAtomic):

    def __init__(self, uid: str, seh, name: str, duration: int, cost: int, calibration_duration: int, calibration_steps: int, calibration_cost: int, error_type: str, test_rate: int):
        CalibratedAtomic.__init__(self, uid, seh, name, duration, cost, calibration_duration, calibration_steps, calibration_cost)
        self._with_error = 0
        self._without_error = 0
        self._errors_found = 0
        self._errors_missed = 0
        self._error_type = error_type
        self._test_rate = test_rate
        self._cnt = 1
    
    def get_stats(self) -> Dict[str, Any]:
        stats = CalibratedAtomic.get_stats(self)
        stats[TYPE] = TEST
        stats[WITH_ERROR_COUNT] = self._with_error
        stats[WITHOUT_ERROR_COUNT] = self._without_error
        stats[ERRORS_FOUND] = self._errors_found
        stats[ERRORS_MISSED] = self._errors_missed
        return stats

    def _do_process(self) -> None:
        resource = self._loaded_input[0]
        will_test = (self._cnt % self._test_rate) == 0
        self._cnt += 1
        has_error_stream = self._output_streams[0]
        ok_stream = self._output_streams[1]

        if not will_test:
            if resource.has_error(self._error_type):
                self._errors_missed += 1
                self._with_error += 1
            else:
                self._without_error += 1
            self._runs -= 1
            ok_stream.try_load(resource)
            return

        if resource.has_error(self._error_type):
            self._errors_found += 1
            self._with_error += 1
            has_error_stream.try_load(resource)
        else:
            ok_stream.try_load(resource)
            self._without_error += 1
