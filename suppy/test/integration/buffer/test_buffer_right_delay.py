from suppy.simulator.atomics.buffer_atomic import BufferAtomic
from suppy.utils.stats_constants import ACTIVE_TIME, BUFFER, CAPACITY, HAS_CALIBRATION, IDLE_TIME, NAME, NOT_USED_RESOURCES, RESOURCE_COUNT, TOTAL_ACTIVE_COST, TRANSPORT, TYPE, VALID_RESOURCE_COUNT, WAS_FULL
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.resource_stream import ResourceStream
from suppy.simulator.atomics.end_atomic import EndAtomic
from suppy.simulator.atomics.transport_atomic import TransportAtomic
from suppy.simulator.atomics.start_atomic import StartAtomic
from suppy.simulator.event_handler import EventHandler


def test_buffer_right_delay():
    name_start = 'start'
    name_buffer = 'buffer'
    name_end = 'end'
    name_transport = 'transport'
    cost = 5
    duration = 10
    resource_type = 'type'
    capacity = 5
    resource_count = 500
    uid_start = 's'
    uid_buffer = 'b'
    uid_end = 'e'
    uid_transport = 't'

    seh = EventHandler()
    start_atomic = StartAtomic(uid_start, seh, name_start, resource_type, resource_count)
    buffer_atomic = BufferAtomic(uid_buffer, seh, name_buffer, capacity)
    transport_atomic = TransportAtomic(uid_transport, seh, name_transport, duration, cost)
    end_atomic = EndAtomic(uid_end, seh, name_end)

    start_buffer_stream = ResourceStream(start_atomic, buffer_atomic)
    buffer_transport_stream = ResourceStream(buffer_atomic, transport_atomic)
    transport_end_stream = ResourceStream(transport_atomic, end_atomic)

    start_atomic.register_output_stream(start_buffer_stream)

    buffer_atomic.register_input_stream(start_buffer_stream)
    buffer_atomic.register_output_stream(buffer_transport_stream)

    transport_atomic.register_input_stream(buffer_transport_stream)
    transport_atomic.register_output_stream(transport_end_stream)

    end_atomic.register_input_stream(transport_end_stream)

    network = AtomicNetwork()
    network.add_atomic(start_atomic)
    network.add_atomic(buffer_atomic)
    network.add_atomic(end_atomic)
    network.add_atomic(transport_atomic)
    network.mark_as_start(uid_start)

    seh.run_on_network(network)

    start_stats = start_atomic.get_stats()
    assert start_stats[NOT_USED_RESOURCES] == 0

    buffer_stats = buffer_atomic.get_stats()
    assert buffer_stats[HAS_CALIBRATION] == False
    assert buffer_stats[WAS_FULL] == True
    assert buffer_stats[CAPACITY] == capacity
    assert buffer_stats[TYPE] == BUFFER
    assert buffer_stats[NAME] == name_buffer

    end_stats = end_atomic.get_stats()
    assert end_stats[RESOURCE_COUNT] == resource_count
    assert end_stats[VALID_RESOURCE_COUNT] == resource_count

test_buffer_right_delay()