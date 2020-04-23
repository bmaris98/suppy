import pytest
from suppy.utils.stats_constants import ERRORS, ERRORS_FOUND, ERRORS_MISSED, RESOURCE_COUNT, TOTAL_CALIBRATION_COST, WITHOUT_ERROR_COUNT, WITH_ERROR_COUNT
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.resource_stream import ResourceStream
from suppy.simulator.atomics.end_atomic import EndAtomic
from suppy.simulator.atomics.start_atomic import StartAtomic
from suppy.simulator.atomics.random_error_atomic import RandomErrorAtomic
from suppy.simulator.atomics.verification_atomic import VerificationAtomic
from suppy.simulator.event_handler import EventHandler


def test_atomic_50():

    rate = 0.5
    duration = 10
    cost = 200
    calibration_cost = 500
    calibration_duration = 40
    calibration_steps = 50
    error_type = 'ERR'
    start_uid = 'start'
    resource_count = 500
    resource_type = 'type'
    seh = EventHandler()

    start_atomic = StartAtomic(start_uid, seh, 'start', resource_type, resource_count)
    error_atomic = RandomErrorAtomic('rnd', seh, 'random_error', error_type, rate)
    test_atomic = VerificationAtomic('test', seh, 'test', duration, cost, calibration_duration, calibration_steps, calibration_cost, error_type, 1)
    end_error = EndAtomic('end_error', seh, 'end0')
    end_ok = EndAtomic('end_ok', seh, 'end1')

    start_error_stream = ResourceStream(start_atomic, error_atomic)
    error_test_stream = ResourceStream(error_atomic, test_atomic)
    test_end_error_stream = ResourceStream(test_atomic, end_error)
    test_end_ok_stream = ResourceStream(test_atomic, end_ok)

    start_atomic.register_output_stream(start_error_stream)

    error_atomic.register_input_stream(start_error_stream)
    error_atomic.register_output_stream(error_test_stream)

    test_atomic.register_input_stream(error_test_stream)
    test_atomic.register_output_stream(test_end_error_stream)
    test_atomic.register_output_stream(test_end_ok_stream)

    end_error.register_input_stream(test_end_error_stream)

    end_ok.register_input_stream(test_end_ok_stream)

    network = AtomicNetwork()
    network.add_atomic(start_atomic)
    network.add_atomic(error_atomic)
    network.add_atomic(test_atomic)
    network.add_atomic(end_error)
    network.add_atomic(end_ok)
    network.mark_as_start(start_atomic.uid)

    seh.run_on_network(network)

    test_stats = test_atomic.get_stats()
    end_error_stats = end_error.get_stats()
    end_ok_stats = end_ok.get_stats()

    assert not end_error_stats[RESOURCE_COUNT] == 0
    assert not end_ok_stats[RESOURCE_COUNT] == 0
    assert end_error_stats[RESOURCE_COUNT] == test_stats[WITH_ERROR_COUNT]
    assert end_ok_stats[RESOURCE_COUNT] == test_stats[WITHOUT_ERROR_COUNT]
    assert end_ok_stats[RESOURCE_COUNT] + end_error_stats[RESOURCE_COUNT] == resource_count
    assert test_stats[TOTAL_CALIBRATION_COST] == calibration_cost * 10
    assert test_stats[ERRORS_MISSED] == 0
    assert test_stats[ERRORS_FOUND] == end_error_stats[RESOURCE_COUNT]

def test_atomic_100_2():

    rate = 0.5
    duration = 10
    cost = 200
    calibration_cost = 500
    calibration_duration = 40
    calibration_steps = 50
    error_type = 'ERR'
    start_uid = 'start'
    resource_count = 1000
    resource_type = 'type'
    seh = EventHandler()

    start_atomic = StartAtomic(start_uid, seh, 'start', resource_type, resource_count)
    error_atomic = RandomErrorAtomic('rnd', seh, 'random_error', error_type, rate)
    test_atomic = VerificationAtomic('test', seh, 'test', duration, cost, calibration_duration, calibration_steps, calibration_cost, error_type, 2)
    end_error = EndAtomic('end_error', seh, 'end0')
    end_ok = EndAtomic('end_ok', seh, 'end1')

    start_error_stream = ResourceStream(start_atomic, error_atomic)
    error_test_stream = ResourceStream(error_atomic, test_atomic)
    test_end_error_stream = ResourceStream(test_atomic, end_error)
    test_end_ok_stream = ResourceStream(test_atomic, end_ok)

    start_atomic.register_output_stream(start_error_stream)

    error_atomic.register_input_stream(start_error_stream)
    error_atomic.register_output_stream(error_test_stream)

    test_atomic.register_input_stream(error_test_stream)
    test_atomic.register_output_stream(test_end_error_stream)
    test_atomic.register_output_stream(test_end_ok_stream)

    end_error.register_input_stream(test_end_error_stream)

    end_ok.register_input_stream(test_end_ok_stream)

    network = AtomicNetwork()
    network.add_atomic(start_atomic)
    network.add_atomic(error_atomic)
    network.add_atomic(test_atomic)
    network.add_atomic(end_error)
    network.add_atomic(end_ok)
    network.mark_as_start(start_atomic.uid)

    seh.run_on_network(network)

    test_stats = test_atomic.get_stats()
    end_error_stats = end_error.get_stats()
    end_ok_stats = end_ok.get_stats()

    assert not end_error_stats[RESOURCE_COUNT] == 0
    assert not end_ok_stats[RESOURCE_COUNT] == 0
    assert end_error_stats[RESOURCE_COUNT] == test_stats[ERRORS_FOUND]
    assert end_ok_stats[RESOURCE_COUNT] == resource_count - test_stats[ERRORS_FOUND]
    assert end_ok_stats[RESOURCE_COUNT] + end_error_stats[RESOURCE_COUNT] == resource_count
    assert test_stats[TOTAL_CALIBRATION_COST] == calibration_cost * 20 / 2
    assert test_stats[ERRORS_MISSED] == test_stats[WITH_ERROR_COUNT] - test_stats[ERRORS_FOUND]
    assert test_stats[ERRORS_FOUND] / resource_count == pytest.approx(1/4, 0.1)
    assert end_ok_stats[ERRORS][error_type] / resource_count == pytest.approx(1/4, 0.1)