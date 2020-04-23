from copy import deepcopy
from typing import Optional
from suppy.simulator.notification import Notification
from suppy.simulator.exceptions.InvalidResourceCategoryException import InvalidResourceCategoryException
from suppy.models.resource import Resource

class ResourceStream:

    def __init__(self, origin, target):
        self._origin = origin
        self._target = target
        self._input_pin: Optional[Resource] = None
        self._output_pin: Optional[Resource] = None

    def try_load(self, resource: Resource): 
        if not self._input_pin == None:
            return False
        self._input_pin = resource
        self._target.notify(self, Notification.INPUT_STREAM_HAS_INPUT)
        return True

    def try_transfer(self):
        if self._input_pin == None:
            return False
        if not self._output_pin == None:
            return False
        self._output_pin = deepcopy(self._input_pin)
        self._input_pin = None
        self._target.notify(self, Notification.INPUT_STREAM_TRANSFER_COMPLETE)
        self._origin.notify(self, Notification.OUTPUT_STREAM_TRANSFER_COMPLETE)
        return True

    @property
    def has_output(self):
        return not self._output_pin == None

    @property
    def has_input(self):
        return not self._input_pin == None

    def consume(self) -> Resource:
        val: Optional[Resource] = deepcopy(self._output_pin)
        self._output_pin = None
        self._origin.notify(self, Notification.OUTPUT_STREAM_CONSUMED)
        if not val == None:
            return val
        raise Exception("None output in stream.")
        