from suppy.simulator.atomics.repair_atomic import RepairAtomic
from suppy.utils.stats_constants import ERRORS, NON_REPAIRS, NOT_USED_RESOURCES, RANDOM_ERROR, REPAIR, REPAIRS, RESOURCE_COUNT, TOTAL_ACTIVE_COST, TOTAL_CALIBRATION_COST, TYPE, VALID_RESOURCE_COUNT
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.resource_stream import ResourceStream
from suppy.simulator.atomics.end_atomic import EndAtomic
from suppy.simulator.atomics.random_error_atomic import RandomErrorAtomic
from suppy.simulator.atomics.start_atomic import StartAtomic
from suppy.simulator.event_handler import EventHandler


def test_random_error_repair_100():
    seh = EventHandler()

    start_uid = 's'
    random_uid = 'r'
    calibration_duration = 100
    calibration_steps = 10
    calibration_cost = 300
    duration = 5
    cost = 1
    repair_uid = 'repair'
    end_uid = 'e'
    start_name = 'start'
    random_name = 'random'
    repair_name = 'repair atomic'
    end_name = 'end'

    resource_type = 'type'
    resource_count = 100

    rate = 1
    error = 'ERR'

    start_atomic = StartAtomic(start_uid, seh, start_name, resource_type, resource_count)
    random_atomic = RandomErrorAtomic(random_uid, seh, random_name, error, rate)
    repair_atomic = RepairAtomic(repair_uid, seh, repair_name, duration, cost, calibration_duration, calibration_steps, calibration_cost, error)
    end_atomic = EndAtomic(end_uid, seh, end_name)

    start_random_stream = ResourceStream(start_atomic, random_atomic)
    random_repair_stream = ResourceStream(random_atomic, repair_atomic)
    repair_end_stream = ResourceStream(repair_atomic, end_atomic)
    
    start_atomic.register_output_stream(start_random_stream)

    random_atomic.register_input_stream(start_random_stream)
    random_atomic.register_output_stream(random_repair_stream)

    repair_atomic.register_input_stream(random_repair_stream)
    repair_atomic.register_output_stream(repair_end_stream)

    end_atomic.register_input_stream(repair_end_stream)
    
    network = AtomicNetwork()
    network.add_atomic(start_atomic)
    network.add_atomic(random_atomic)
    network.add_atomic(end_atomic)
    network.add_atomic(repair_atomic)
    network.mark_as_start(start_uid)

    seh.run_on_network(network)

    start_stats = start_atomic.get_stats()
    assert start_stats[NOT_USED_RESOURCES] == 0

    random_stats = random_atomic.get_stats()
    assert random_stats[TYPE] == RANDOM_ERROR

    repair_stats = repair_atomic.get_stats()
    assert repair_stats[TYPE] == REPAIR
    assert repair_stats[REPAIRS] == resource_count
    assert repair_stats[NON_REPAIRS] == 0
    assert repair_stats[TOTAL_CALIBRATION_COST] == calibration_cost * 10

    end_stats = end_atomic.get_stats()
    assert end_stats[RESOURCE_COUNT] == resource_count
    assert end_stats[VALID_RESOURCE_COUNT] == resource_count
    assert error not in end_stats[ERRORS]

def test_random_error_repair_0():
    seh = EventHandler()

    start_uid = 's'
    random_uid = 'r'
    calibration_duration = 100
    calibration_steps = 10
    calibration_cost = 300
    duration = 5
    cost = 1
    repair_uid = 'repair'
    end_uid = 'e'
    start_name = 'start'
    random_name = 'random'
    repair_name = 'repair atomic'
    end_name = 'end'

    resource_type = 'type'
    resource_count = 100

    rate = 0
    error = 'ERR'

    start_atomic = StartAtomic(start_uid, seh, start_name, resource_type, resource_count)
    random_atomic = RandomErrorAtomic(random_uid, seh, random_name, error, rate)
    repair_atomic = RepairAtomic(repair_uid, seh, repair_name, duration, cost, calibration_duration, calibration_steps, calibration_cost, error)
    end_atomic = EndAtomic(end_uid, seh, end_name)

    start_random_stream = ResourceStream(start_atomic, random_atomic)
    random_repair_stream = ResourceStream(random_atomic, repair_atomic)
    repair_end_stream = ResourceStream(repair_atomic, end_atomic)
    
    start_atomic.register_output_stream(start_random_stream)

    random_atomic.register_input_stream(start_random_stream)
    random_atomic.register_output_stream(random_repair_stream)

    repair_atomic.register_input_stream(random_repair_stream)
    repair_atomic.register_output_stream(repair_end_stream)

    end_atomic.register_input_stream(repair_end_stream)
    
    network = AtomicNetwork()
    network.add_atomic(start_atomic)
    network.add_atomic(random_atomic)
    network.add_atomic(end_atomic)
    network.add_atomic(repair_atomic)
    network.mark_as_start(start_uid)

    seh.run_on_network(network)

    start_stats = start_atomic.get_stats()
    assert start_stats[NOT_USED_RESOURCES] == 0

    random_stats = random_atomic.get_stats()
    assert random_stats[TYPE] == RANDOM_ERROR

    repair_stats = repair_atomic.get_stats()
    assert repair_stats[TYPE] == REPAIR
    assert repair_stats[REPAIRS] == 0
    assert repair_stats[NON_REPAIRS] == resource_count
    assert repair_stats[TOTAL_CALIBRATION_COST] == calibration_cost * 10

    end_stats = end_atomic.get_stats()
    assert end_stats[RESOURCE_COUNT] == resource_count
    assert end_stats[VALID_RESOURCE_COUNT] == resource_count
    assert error not in end_stats[ERRORS]