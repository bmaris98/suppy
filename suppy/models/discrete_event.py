from suppy.simulator.atomics.atomic import Atomic
from suppy.simulator.atomics.atomic_states import AtomicStates


class DiscreteEvent:

    def __init__(self, state: AtomicStates, atomic: Atomic):
        self._state = state
        self._atomic = atomic

    @property
    def state(self):
        return self._state

    @property
    def atomic(self):
        return self._atomic