from suppy.utils.stats_constants import RESOURCE_COUNT, RUNS
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.resource_stream import ResourceStream
from suppy.simulator.atomics.end_atomic import EndAtomic
from suppy.simulator.atomics.convergence_atomic import ConvergenceAtomic
from suppy.simulator.atomics.divergence_atomic import DivergenceAtomic
from suppy.simulator.atomics.transport_atomic import TransportAtomic
from suppy.simulator.atomics.start_atomic import StartAtomic
from suppy.simulator.event_handler import EventHandler


def test_divergence():

    seh = EventHandler()
    cost = 20
    duration = 40
    resource_type = 'type'
    resource_count = 200

    start = StartAtomic('start_uid', seh, 'start', resource_type, resource_count)
    divergence = DivergenceAtomic('div_uid', seh, 'div')
    t1 = TransportAtomic('t1', seh, 't1', duration, cost)
    t2 = TransportAtomic('t2', seh, 't2', duration, cost)
    convergence = ConvergenceAtomic('con', seh, 'con')
    end = EndAtomic('end', seh, 'end')

    start_divergence = ResourceStream(start, divergence)
    divergence_t1 = ResourceStream(divergence, t1)
    divergence_t2 = ResourceStream(divergence, t2)
    t1_conv = ResourceStream(t1, convergence)
    t2_conv = ResourceStream(t2, convergence)
    conv_end = ResourceStream(convergence, end)

    start.register_output_stream(start_divergence)

    divergence.register_input_stream(start_divergence)
    divergence.register_output_stream(divergence_t1)
    divergence.register_output_stream(divergence_t2)

    t1.register_input_stream(divergence_t1)
    t1.register_output_stream(t1_conv)

    t2.register_input_stream(divergence_t2)
    t2.register_output_stream(t2_conv)

    convergence.register_input_stream(t1_conv)
    convergence.register_input_stream(t2_conv)
    convergence.register_output_stream(conv_end)

    end.register_input_stream(conv_end)

    network = AtomicNetwork()

    network.add_atomic(start)
    network.add_atomic(divergence)
    network.add_atomic(t1)
    network.add_atomic(t2)
    network.add_atomic(convergence)
    network.add_atomic(end)
    network.mark_as_start(start.uid)

    seh.run_on_network(network)

    t1_stats = t1.get_stats()
    t2_stats = t2.get_stats()
    end_stats = end.get_stats()
    
    assert t1_stats[RUNS] == resource_count/2
    assert t2_stats[RUNS] == resource_count/2
    assert end_stats[RESOURCE_COUNT] == resource_count