from suppy.utils.stats_constants import ACTIVE_TIME, HAS_CALIBRATION, IDLE_TIME, NAME, NOT_USED_RESOURCES, RESOURCE_COUNT, TOTAL_ACTIVE_COST, TRANSPORT, TYPE, VALID_RESOURCE_COUNT
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.resource_stream import ResourceStream
from suppy.simulator.atomics.end_atomic import EndAtomic
from suppy.simulator.atomics.transport_atomic import TransportAtomic
from suppy.simulator.atomics.start_atomic import StartAtomic
from suppy.simulator.event_handler import EventHandler

def test_transport():
    name_start = 'start'
    name_transport = 'transport'
    name_end = 'end'
    resource_type = 'type'
    duration = 100
    cost = 200
    resource_count = 2
    uid_start = 's'
    uid_transport = 't'
    uid_end = 'e'

    seh = EventHandler()
    start_atomic = StartAtomic(uid_start, seh, name_start, resource_type, resource_count)
    transport_atomic = TransportAtomic(uid_transport, seh, name_transport, duration, cost)
    end_atomic = EndAtomic(uid_end, seh, name_end)

    start_transport_stream = ResourceStream(start_atomic, transport_atomic)
    transport_end_stream = ResourceStream(transport_atomic, end_atomic)

    start_atomic.register_output_stream(start_transport_stream)

    transport_atomic.register_input_stream(start_transport_stream)
    transport_atomic.register_output_stream(transport_end_stream)

    end_atomic.register_input_stream(transport_end_stream)

    network = AtomicNetwork()
    network.add_atomic(start_atomic)
    network.add_atomic(transport_atomic)
    network.add_atomic(end_atomic)
    network.mark_as_start(uid_start)

    seh.run_on_network(network)

    start_stats = start_atomic.get_stats()
    assert start_stats[NOT_USED_RESOURCES] == 0

    transport_stats = transport_atomic.get_stats()
    assert transport_stats[ACTIVE_TIME] == resource_count * duration
    assert transport_stats[IDLE_TIME] == 0
    assert transport_stats[TOTAL_ACTIVE_COST] == resource_count * cost
    assert transport_stats[HAS_CALIBRATION] == False
    assert transport_stats[TYPE] == TRANSPORT
    assert transport_stats[NAME] == name_transport

    end_stats = end_atomic.get_stats()
    assert end_stats[RESOURCE_COUNT] == resource_count
    assert end_stats[VALID_RESOURCE_COUNT] == resource_count