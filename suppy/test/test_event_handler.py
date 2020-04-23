# from suppy.simulator.atomics.atomic import Atomic
# from suppy.simulator.atomics.atomic_states import AtomicStates
# from suppy.models.discrete_event import DiscreteEvent
# from suppy.models.time_point import TimePoint
# from suppy.simulator.event_handler import EventHandler


# # atomic = Atomic

# # class TestEventHandler:

# #     def test_queue_deque(self):
# #         handler = EventHandler()
# #         t1 = (TimePoint(100, 1), DiscreteEvent(AtomicStates.READY, None))
# #         t2 = (TimePoint(1, 2), DiscreteEvent(AtomicStates.CALIBRATING))
# #         t3 = (TimePoint(1, 1), DiscreteEvent(AtomicStates.ACTIVE))

# #         handler.queue_event(t1[0], t1[1])
# #         handler.queue_event(t2[0], t2[1])
# #         handler.queue_event(t3[0], t3[1])

# #         time_point, event = handler.deque_event()
# #         assert time_point == TimePoint(1, 1)
# #         assert event.event_type == 'ydecision'

# #         time_point, event = handler.deque_event()
# #         assert time_point == TimePoint(1, 2)
# #         assert event.event_type == 'zdecision'

# #         time_point, event = handler.deque_event()
# #         assert time_point == TimePoint(100, 1)
# #         assert event.event_type == 'decision'

# #     def test_peek_event(self):
# #         handler = EventHandler()
# #         t2 = (TimePoint(1, 2), DiscreteEvent('zdecision'))
# #         t1 = (TimePoint(100, 1), DiscreteEvent('decision'))

# #         handler.queue_event(t1[0], t1[1])
# #         handler.queue_event(t2[0], t2[1])

# #         time_point, event = handler.peek_event()
# #         assert time_point == TimePoint(1, 2)
# #         assert event.event_type == 'zdecision'

# #         event._event_type = 'err' # make sure it copy works

# #         time_point, event = handler.peek_event()
# #         assert time_point == TimePoint(1, 2)
# #         assert event.event_type == 'zdecision'

# #     def test_has_events(self):
# #         handler = EventHandler()
        
# #         assert handler.has_events() == False

# #         handler.queue_event(TimePoint(1,1), DiscreteEvent('a'))

# #         assert handler.has_events() == True
# #         assert handler.has_events() == True # does not modify state

# #     def test_monostate(self):
# #         h1 = EventHandler()
# #         h2 = EventHandler()
# #         assert h1.has_events() == False
# #         assert h2.has_events() == False

# #         tp = TimePoint(1, 1)
# #         de = DiscreteEvent('a')
# #         h1.queue_event(tp, de)
# #         assert h2.has_events() == True
# #         actual_tp, actual_de = h2.deque_event()

# #         assert actual_tp == tp
# #         assert actual_de.event_type == de.event_type
