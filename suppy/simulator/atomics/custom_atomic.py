from typing import Any, Dict
from suppy.utils.stats_constants import CUSTOM, TYPE
from suppy.models.resource import Resource
from suppy.simulator.atomics.calibrated_atomic import CalibratedAtomic


class CustomAtomic(CalibratedAtomic):

    def __init__(self, uid: str, seh, name: str, duration: int, cost: int, calibration_duration: int, calibration_steps: int, calibration_cost: int, output_type: str):
        CalibratedAtomic.__init__(self, uid, seh, name, duration, cost, calibration_duration, calibration_steps, calibration_cost)
        self._output_type = output_type

    def _do_process(self) -> None:
        resource = Resource(self._output_type)
        for input_resource in self._loaded_input:
            for error in input_resource.errors:
                resource.add_error(error)
        self._output_streams[0].try_load(resource)

    def get_stats(self) -> Dict[str, Any]:
        stats = CalibratedAtomic.get_stats(self)
        stats[TYPE] = CUSTOM
        return stats