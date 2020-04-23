from suppy.utils.stats_constants import ACTIVE_TIME, CALIBRATION_COUNT, CALIBRATION_LEFT, CALIBRATION_TIME, CUSTOM, END, ERRORS, HAS_CALIBRATION, IDLE_TIME, NAME, NOT_USED_RESOURCES, RESOURCE_COUNT, RESOURCE_TYPE, START, TOTAL_ACTIVE_COST, TOTAL_CALIBRATION_COST, TYPE, VALID_RESOURCE_COUNT
from suppy.simulator.event_handler import EventHandler
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.resource_stream import ResourceStream
from suppy.simulator.atomics.custom_atomic import CustomAtomic
from suppy.simulator.atomics.end_atomic import EndAtomic
from suppy.simulator.atomics.start_atomic import StartAtomic


def test_single_input():

    type1 = 'A'
    type2 = 'B'
    uid_start = '1'
    uid_custom = '2'
    uid_end = '3'
    resource_count = 41
    calibration_cost = 5
    duration = 100
    cost = 5
    calibration_time = 40
    calibration_steps = 10

    seh = EventHandler()

    start_atomic = StartAtomic(uid_start, seh, 'Start Node', type1, resource_count)
    custom_atomic = CustomAtomic(uid_custom, seh, 'Custom Node', duration, cost, calibration_time, calibration_steps, calibration_cost, type2)
    end_atomic = EndAtomic(uid_end, seh, 'End Node')

    start_custom_stream = ResourceStream(start_atomic, custom_atomic)
    custom_end_stream = ResourceStream(custom_atomic, end_atomic)

    start_atomic.register_output_stream(start_custom_stream)
    custom_atomic.register_input_stream(start_custom_stream)
    custom_atomic.register_output_stream(custom_end_stream)
    end_atomic.register_input_stream(custom_end_stream)

    network = AtomicNetwork()
    network.add_atomic(start_atomic)
    network.add_atomic(custom_atomic)
    network.add_atomic(end_atomic)
    network.mark_as_start(uid_start)

    seh.run_on_network(network)

    start_stats = start_atomic.get_stats()
    assert start_stats[NAME] == 'Start Node'
    assert start_stats[TYPE] == START
    assert start_stats[RESOURCE_COUNT] == resource_count
    assert start_stats[HAS_CALIBRATION] == False
    assert start_stats[NOT_USED_RESOURCES] == 0
    assert start_stats[RESOURCE_TYPE] == type1

    custom_stats = custom_atomic.get_stats()
    assert custom_stats[NAME] == 'Custom Node'
    assert custom_stats[TYPE] == CUSTOM
    assert custom_stats[TOTAL_CALIBRATION_COST] == calibration_cost * 4
    assert custom_stats[HAS_CALIBRATION] == True
    assert custom_stats[ACTIVE_TIME] == duration * resource_count
    assert custom_stats[TOTAL_ACTIVE_COST] == resource_count * cost
    assert custom_stats[IDLE_TIME] == 0
    assert custom_stats[CALIBRATION_COUNT] == 4
    assert custom_stats[CALIBRATION_LEFT] == 9
    assert custom_stats[CALIBRATION_TIME] == 4 * calibration_time

    end_stats = end_atomic.get_stats()
    assert end_stats[NAME] == 'End Node'
    assert end_stats[TYPE] == END
    assert end_stats[RESOURCE_COUNT] == resource_count
    assert end_stats[VALID_RESOURCE_COUNT] == resource_count
    assert len(end_stats[ERRORS]) == 0
    assert start_stats[HAS_CALIBRATION] == False

    assert seh.time == duration * resource_count + 4 * calibration_time
