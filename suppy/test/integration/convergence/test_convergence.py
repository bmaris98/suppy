from suppy.utils.stats_constants import RESOURCE_COUNT
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.resource_stream import ResourceStream
from suppy.simulator.atomics.transport_atomic import TransportAtomic
from suppy.simulator.atomics.end_atomic import EndAtomic
from suppy.simulator.atomics.convergence_atomic import ConvergenceAtomic
from suppy.simulator.atomics.start_atomic import StartAtomic
from suppy.simulator.event_handler import EventHandler


def test_convergence():
    seh = EventHandler()

    start1_uid = 'start1'
    start2_uid = 'start2'
    resource_type = 'resource_type'
    resource_count = 100

    start1 = StartAtomic(start1_uid, seh, 'start1', resource_type, resource_count)
    start2 = StartAtomic(start2_uid, seh, 'start2', resource_type, resource_count)
    convergence = ConvergenceAtomic('conv', seh, 'conv')
    transport = TransportAtomic('tr', seh, 'trns', 20, 20)
    end = EndAtomic('end', seh, 'end')

    start1_conv_stream = ResourceStream(start1, convergence)
    start2_conv_stream = ResourceStream(start2, convergence)
    conv_transport_stream = ResourceStream(convergence, transport)
    transport_end_stream = ResourceStream(transport, end)

    start1.register_output_stream(start1_conv_stream)
    start2.register_output_stream(start2_conv_stream)

    convergence.register_input_stream(start1_conv_stream)
    convergence.register_input_stream(start2_conv_stream)
    convergence.register_output_stream(conv_transport_stream)

    transport.register_input_stream(conv_transport_stream)
    transport.register_output_stream(transport_end_stream)

    end.register_input_stream(transport_end_stream)
    
    network = AtomicNetwork()
    network.add_atomic(start1)
    network.add_atomic(start2)
    network.add_atomic(convergence)
    network.add_atomic(transport)
    network.add_atomic(end)
    network.mark_as_start(start1.uid)
    network.mark_as_start(start2.uid)

    seh.run_on_network(network)
    
    end_stats = end.get_stats()
    assert end_stats[RESOURCE_COUNT] == 2* resource_count

test_convergence()

def test_convergence_decalated():
    seh = EventHandler()

    start1_uid = 'start1'
    start2_uid = 'start2'
    resource_type = 'resource_type'
    resource_count = 100

    start1 = StartAtomic(start1_uid, seh, 'start1', resource_type, resource_count)
    start2 = StartAtomic(start2_uid, seh, 'start2', resource_type, resource_count)
    convergence = ConvergenceAtomic('conv', seh, 'conv')
    transport1 = TransportAtomic('tr2', seh, 'trns2', 20, 20)
    transport2 = TransportAtomic('tr3', seh, 'trns3', 10, 20)
    transport3 = TransportAtomic('tr', seh, 'trns', 200, 20)
    end = EndAtomic('end', seh, 'end')

    start1_transport1 = ResourceStream(start1, transport1)
    start2_transport2 = ResourceStream(start2, transport2)
    transport1_conv = ResourceStream(transport1, convergence)
    transport2_conv = ResourceStream(transport2, convergence)
    conv_transport3 = ResourceStream(convergence, transport3)
    transport3_end = ResourceStream(transport3, end)

    start1.register_output_stream(start1_transport1)
    start2.register_output_stream(start2_transport2)

    transport1.register_input_stream(start1_transport1)
    transport1.register_output_stream(transport1_conv)

    transport2.register_input_stream(start2_transport2)
    transport2.register_output_stream(transport2_conv)

    convergence.register_input_stream(transport1_conv)
    convergence.register_input_stream(transport2_conv)
    convergence.register_output_stream(conv_transport3)

    transport3.register_input_stream(conv_transport3)
    transport3.register_output_stream(transport3_end)

    end.register_input_stream(transport3_end)
    
    network = AtomicNetwork()
    network.add_atomic(start1)
    network.add_atomic(start2)
    network.add_atomic(convergence)
    network.add_atomic(transport1)
    network.add_atomic(transport2)
    network.add_atomic(transport3)
    network.add_atomic(end)
    network.mark_as_start(start1.uid)
    network.mark_as_start(start2.uid)

    seh.run_on_network(network)
    
    end_stats = end.get_stats()
    assert end_stats[RESOURCE_COUNT] == 2 * resource_count