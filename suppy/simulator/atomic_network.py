from suppy.simulator.atomics.atomic import Atomic
from typing import Any, Dict, List, Set


class AtomicNetwork:

    def __init__(self):
        self._atomics: Dict[str, Atomic] = {}
        self._start_uids: Set[str] = set()

    def add_atomic(self, atomic: Atomic) -> None:
        self._atomics[atomic.uid] = atomic

    def mark_as_start(self, atomic_uid: str) -> None:
        self._start_uids.add(atomic_uid)

    def get_atomic_by_uid(self, atomic_uid: str) -> Atomic:
        return self._atomics[atomic_uid]

    def get_stats(self) -> List[Dict[str, Any]]:
        stats = []
        for _, atomic in self._atomics.items():
            stats.append(atomic.get_stats())
        return stats

    @property
    def start_atomics(self) -> List[Atomic]:
        start_atomics = []
        for uid in self._start_uids:
            start_atomics.append(self._atomics[uid])
        return start_atomics