from copy import deepcopy
from suppy.utils.stats_constants import END, ERRORS, RESOURCE_COUNT, TYPE, VALID_RESOURCE_COUNT
from suppy.models.resource import Resource
from suppy.simulator.atomics.atomic import Atomic
from typing import Any, Dict, List

class EndAtomic(Atomic):

    def __init__(self, uid: str, seh, name: str):
        Atomic.__init__(self, uid, seh, name, 0, 0)
        self._name: str = name
        self._resources: List[Resource] = []

    def _do_process(self) -> None:
        resource = deepcopy(self._loaded_input[0])
        self._resources.append(resource)

    def get_stats(self) -> Dict[str, Any]:
        stats = Atomic.get_stats(self)
        stats[TYPE] = END
        stats[RESOURCE_COUNT] = self._get_resource_count()
        stats[VALID_RESOURCE_COUNT] = self._get_valid_resource_count()
        stats[ERRORS] = self._get_errors()

        return stats

    def _get_resource_count(self) -> int:
        return len(self._resources)

    def _get_valid_resource_count(self) -> int:
        count = 0
        for resource in self._resources:
            if resource.is_valid:
                count += 1
        return count

    def _get_errors(self) -> Dict[str, int]:
        errors = {}
        for resource in self._resources:
            for error in resource.errors:
                if not error in errors:
                    errors[error] = 1
                else:
                    errors[error] += 1
        return errors