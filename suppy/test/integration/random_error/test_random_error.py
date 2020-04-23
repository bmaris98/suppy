import pytest

from suppy.utils.stats_constants import ERRORS, NOT_USED_RESOURCES, RANDOM_ERROR, RESOURCE_COUNT, TYPE, VALID_RESOURCE_COUNT
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.resource_stream import ResourceStream
from suppy.simulator.atomics.end_atomic import EndAtomic
from suppy.simulator.atomics.random_error_atomic import RandomErrorAtomic
from suppy.simulator.atomics.start_atomic import StartAtomic
from suppy.simulator.event_handler import EventHandler


def test_random_error_100():
    seh = EventHandler()

    start_uid = 's'
    random_uid = 'r'
    end_uid = 'e'
    start_name = 'start'
    random_name = 'random'
    end_name = 'end'

    resource_type = 'type'
    resource_count = 1000

    rate = 1
    error = 'ERR'

    start_atomic = StartAtomic(start_uid, seh, start_name, resource_type, resource_count)
    random_atomic = RandomErrorAtomic(random_uid, seh, random_name, error, rate)
    end_atomic = EndAtomic(end_uid, seh, end_name)

    start_random_stream = ResourceStream(start_atomic, random_atomic)
    random_end_stream = ResourceStream(random_atomic, end_atomic)

    start_atomic.register_output_stream(start_random_stream)

    random_atomic.register_input_stream(start_random_stream)
    random_atomic.register_output_stream(random_end_stream)

    end_atomic.register_input_stream(random_end_stream)
    
    network = AtomicNetwork()
    network.add_atomic(start_atomic)
    network.add_atomic(random_atomic)
    network.add_atomic(end_atomic)
    network.mark_as_start(start_uid)

    seh.run_on_network(network)

    start_stats = start_atomic.get_stats()
    assert start_stats[NOT_USED_RESOURCES] == 0

    random_stats = random_atomic.get_stats()
    assert random_stats[TYPE] == RANDOM_ERROR

    end_stats = end_atomic.get_stats()
    assert end_stats[RESOURCE_COUNT] == resource_count
    assert end_stats[VALID_RESOURCE_COUNT] == 0
    errs = end_stats[ERRORS]
    assert errs[error] == resource_count

def test_random_error_0():
    seh = EventHandler()

    start_uid = 's'
    random_uid = 'r'
    end_uid = 'e'
    start_name = 'start'
    random_name = 'random'
    end_name = 'end'

    resource_type = 'type'
    resource_count = 1000

    rate = 0
    error = 'ERR'

    start_atomic = StartAtomic(start_uid, seh, start_name, resource_type, resource_count)
    random_atomic = RandomErrorAtomic(random_uid, seh, random_name, error, rate)
    end_atomic = EndAtomic(end_uid, seh, end_name)

    start_random_stream = ResourceStream(start_atomic, random_atomic)
    random_end_stream = ResourceStream(random_atomic, end_atomic)

    start_atomic.register_output_stream(start_random_stream)

    random_atomic.register_input_stream(start_random_stream)
    random_atomic.register_output_stream(random_end_stream)

    end_atomic.register_input_stream(random_end_stream)
    
    network = AtomicNetwork()
    network.add_atomic(start_atomic)
    network.add_atomic(random_atomic)
    network.add_atomic(end_atomic)
    network.mark_as_start(start_uid)

    seh.run_on_network(network)

    start_stats = start_atomic.get_stats()
    assert start_stats[NOT_USED_RESOURCES] == 0

    random_stats = random_atomic.get_stats()
    assert random_stats[TYPE] == RANDOM_ERROR

    end_stats = end_atomic.get_stats()
    assert end_stats[RESOURCE_COUNT] == resource_count
    assert end_stats[VALID_RESOURCE_COUNT] == resource_count
    assert error not in end_stats[ERRORS]

def test_random_error_50():
    seh = EventHandler()

    start_uid = 's'
    random_uid = 'r'
    end_uid = 'e'
    start_name = 'start'
    random_name = 'random'
    end_name = 'end'

    resource_type = 'type'
    resource_count = 1000

    rate = 0.5
    error = 'ERR'

    start_atomic = StartAtomic(start_uid, seh, start_name, resource_type, resource_count)
    random_atomic = RandomErrorAtomic(random_uid, seh, random_name, error, rate)
    end_atomic = EndAtomic(end_uid, seh, end_name)

    start_random_stream = ResourceStream(start_atomic, random_atomic)
    random_end_stream = ResourceStream(random_atomic, end_atomic)

    start_atomic.register_output_stream(start_random_stream)

    random_atomic.register_input_stream(start_random_stream)
    random_atomic.register_output_stream(random_end_stream)

    end_atomic.register_input_stream(random_end_stream)
    
    network = AtomicNetwork()
    network.add_atomic(start_atomic)
    network.add_atomic(random_atomic)
    network.add_atomic(end_atomic)
    network.mark_as_start(start_uid)

    seh.run_on_network(network)

    start_stats = start_atomic.get_stats()
    assert start_stats[NOT_USED_RESOURCES] == 0

    random_stats = random_atomic.get_stats()
    assert random_stats[TYPE] == RANDOM_ERROR

    end_stats = end_atomic.get_stats()
    assert end_stats[RESOURCE_COUNT] == resource_count
    valids = end_stats[VALID_RESOURCE_COUNT]
    assert 1 - (valids / resource_count) == pytest.approx(rate, 0.1)
    errors = end_stats[ERRORS][error]
    assert errors + valids == resource_count