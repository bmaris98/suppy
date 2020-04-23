from suppy.utils.prio_queue import PrioQueue


class TestPrioQueue:

    def test_queue(self):
        t1 = (1, 'B')
        t2 = (2, 'C')
        t3 = (3, 'D')
        t4 = (0, 'A')
        t5 = (1, 'B1')
        t6 = (2, 'C1')
        t7 = (4, 'E')
        t8 = (3, 'D1')

        expected_order = [t4, t1, t5, t2, t6, t3, t8, t7]
        pq = PrioQueue()

        assert pq.empty() == True

        pq.queue(t1)
        pq.queue(t2)
        pq.queue(t3)
        pq.queue(t4)
        pq.queue(t5)
        pq.queue(t6)
        pq.queue(t7)
        pq.queue(t8)

        assert pq.empty() == False

        for item in expected_order:
            prio, val = pq.deque()
            assert item[0] == prio
            assert item[1] == val