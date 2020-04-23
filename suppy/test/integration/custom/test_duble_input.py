from suppy.utils.stats_constants import ACTIVE_TIME, CALIBRATION_COUNT, CALIBRATION_LEFT, CALIBRATION_TIME, CUSTOM, END, ERRORS, HAS_CALIBRATION, IDLE_TIME, NAME, NOT_USED_RESOURCES, RESOURCE_COUNT, START, TOTAL_ACTIVE_COST, TOTAL_CALIBRATION_COST, TYPE, VALID_RESOURCE_COUNT
from suppy.simulator.event_handler import EventHandler
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.resource_stream import ResourceStream
from suppy.simulator.atomics.custom_atomic import CustomAtomic
from suppy.simulator.atomics.end_atomic import EndAtomic
from suppy.simulator.atomics.start_atomic import StartAtomic

def test_double_input():

    type1 = 'A1'
    type2 = 'B'
    type3 = 'A2'
    uid_start = '1'
    uid_start2 = '4'
    uid_custom = '2'
    uid_end = '3'
    resource_count1 = 41
    resource_count2 = 42
    calibration_cost = 5
    duration = 100
    cost = 5
    calibration_time = 40
    calibration_steps = 10

    seh = EventHandler()

    start_atomic1 = StartAtomic(uid_start, seh, 'Start Node', type1, resource_count1)
    start_atomic2 = StartAtomic(uid_start2, seh, 'Start Node2', type3, resource_count2)
    custom_atomic = CustomAtomic(uid_custom, seh, 'Custom Node', duration, cost, calibration_time, calibration_steps, calibration_cost, type2)
    end_atomic = EndAtomic(uid_end, seh, 'End Node')

    start_custom_stream = ResourceStream(start_atomic1, custom_atomic)
    start2_custom_stream = ResourceStream(start_atomic2, custom_atomic)
    custom_end_stream = ResourceStream(custom_atomic, end_atomic)

    start_atomic1.register_output_stream(start_custom_stream)
    start_atomic2.register_output_stream(start2_custom_stream)

    custom_atomic.register_input_stream(start_custom_stream)
    custom_atomic.register_input_stream(start2_custom_stream)
    custom_atomic.register_output_stream(custom_end_stream)

    end_atomic.register_input_stream(custom_end_stream)

    network = AtomicNetwork()
    network.add_atomic(start_atomic1)
    network.add_atomic(custom_atomic)
    network.add_atomic(end_atomic)
    network.add_atomic(start_atomic2)
    network.mark_as_start(uid_start)
    network.mark_as_start(uid_start2)

    seh.run_on_network(network)

    start_stats1 = start_atomic1.get_stats()
    assert start_stats1[NAME] == 'Start Node'
    assert start_stats1[TYPE] == START
    assert start_stats1[RESOURCE_COUNT] == resource_count1
    assert start_stats1[HAS_CALIBRATION] == False
    assert start_stats1[NOT_USED_RESOURCES] == 0

    start_stats2 = start_atomic2.get_stats()
    assert start_stats2[NAME] == 'Start Node2'
    assert start_stats2[TYPE] == START
    assert start_stats2[RESOURCE_COUNT] == resource_count2
    assert start_stats2[HAS_CALIBRATION] == False
    assert start_stats2[NOT_USED_RESOURCES] == 1

    custom_stats = custom_atomic.get_stats()
    assert custom_stats[NAME] == 'Custom Node'
    assert custom_stats[TYPE] == CUSTOM
    assert custom_stats[TOTAL_CALIBRATION_COST] == calibration_cost * 4
    assert custom_stats[HAS_CALIBRATION] == True
    assert custom_stats[ACTIVE_TIME] == duration * resource_count1
    assert custom_stats[TOTAL_ACTIVE_COST] == resource_count1 * cost
    assert custom_stats[IDLE_TIME] == 0
    assert custom_stats[CALIBRATION_COUNT] == 4
    assert custom_stats[CALIBRATION_LEFT] == 9
    assert custom_stats[CALIBRATION_TIME] == 4 * calibration_time

    end_stats = end_atomic.get_stats()
    assert end_stats[NAME] == 'End Node'
    assert end_stats[TYPE] == END
    assert end_stats[RESOURCE_COUNT] == resource_count1
    assert end_stats[VALID_RESOURCE_COUNT] == resource_count1
    assert len(end_stats[ERRORS]) == 0
    assert start_stats1[HAS_CALIBRATION] == False

    assert seh.time == duration * resource_count1 + 4 * calibration_time