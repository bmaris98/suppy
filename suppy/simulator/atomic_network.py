from suppy.simulator.atomics.atomic import Atomic
from typing import Dict, List, Set


class AtomicNetwork:

    def __init__(self):
        self._atomics: Dict[str, Atomic] = {}
        self._start_uids: Set[str] = set()

    def add_atomic(self, atomic: Atomic) -> None:
        self._atomics[atomic.uid] = atomic

    def mark_as_start(self, atomic_uid: str) -> None:
        self._start_uids.add(atomic_uid)

    @property
    def start_atomics(self) -> List[Atomic]:
        start_atomics = []
        for uid in self._start_uids:
            start_atomics.append(self._atomics[uid])
        return start_atomics