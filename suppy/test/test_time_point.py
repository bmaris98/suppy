from suppy.models.time_point import TimePoint
from suppy.simulator.atomics.atomic_states import AtomicStates
from suppy.simulator.event_handler import EventHandler

class TestTimePoint:

    def test_comparisons(self):
        assert TimePoint(1, 1) == TimePoint(1, 1)

        assert TimePoint(1, 100) < TimePoint(100, 1)
        assert not TimePoint(1, 1) < TimePoint(1, 1)
        assert TimePoint(1, 1) < TimePoint(1, 2)

        assert TimePoint(1, 1) <= TimePoint(1, 1)
        assert TimePoint(1, 0) <= TimePoint(1, 1)
        assert TimePoint(1, 100) <= TimePoint(2, 0)
        assert not TimePoint(2, 2) <= TimePoint(1, 1)

        assert not TimePoint(1, 1) > TimePoint(1, 1)
        assert TimePoint(100, 1) > TimePoint(10, 1)
        assert TimePoint(1, 100) > TimePoint(1, 10)

        assert TimePoint(1, 1) >= TimePoint(1, 1)
        assert TimePoint(2, 0) >= TimePoint(1, 100)
        assert TimePoint(2, 100) >= TimePoint(2, 10)
        assert not TimePoint(1, 2) >= TimePoint(1,3)  