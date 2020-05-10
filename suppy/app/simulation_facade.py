import json
from pathlib import Path
import datetime
from suppy.app.report_generator import ReportGenerator
from suppy.simulator.resource_stream import ResourceStream
from suppy.utils.stats_constants import BUFFER, CONVERGENCE, CUSTOM, DIVERGENCE, END, RANDOM_ERROR, REPAIR, START, TEST, TRANSPORT
from suppy.simulator.atomics.atomic import Atomic
from suppy.app.node import Node
from typing import List
from suppy.simulator.event_handler import EventHandler
from suppy.simulator.atomic_network import AtomicNetwork
from suppy.simulator.atomics.buffer_atomic import BufferAtomic
from suppy.simulator.atomics.custom_atomic import CustomAtomic
from suppy.simulator.atomics.divergence_atomic import DivergenceAtomic
from suppy.simulator.atomics.end_atomic import EndAtomic
from suppy.simulator.atomics.random_error_atomic import RandomErrorAtomic
from suppy.simulator.atomics.repair_atomic import RepairAtomic
from suppy.simulator.atomics.start_atomic import StartAtomic
from suppy.simulator.atomics.transport_atomic import TransportAtomic
from suppy.simulator.atomics.verification_atomic import VerificationAtomic
from suppy.simulator.atomics.convergence_atomic import ConvergenceAtomic
from suppy.app.line import Line

class SimulationFacade:

    def __init__(self):
        self._atomic_network = AtomicNetwork()
        self._seh = EventHandler()
        self._data_path = Path(__file__).parent / '../data'

    def load_atomics_from_nodes(self, nodes: List[Node]) -> None:
        for node in nodes:
            self._load_atomic_from_node(node)

    def _load_atomic_from_node(self, node: Node) -> None:
        atomic: Atomic = StartAtomic('1', self._seh, 'name', 'type', 1)
        is_start = False
        
        if node.type == BUFFER:
            atomic = self._create_buffer_atomic(node)
        
        if node.type == CONVERGENCE:
            atomic = self._create_convergence_atomic(node)

        if node.type == CUSTOM:
            atomic = self._create_custom_atomic(node)

        if node.type == DIVERGENCE:
            atomic = self._create_divergence_atomic(node)

        if node.type == END:
            atomic = self._create_end_atomic(node)

        if node.type == RANDOM_ERROR:
            atomic = self._create_random_error_atomic(node)

        if node.type == REPAIR:
            atomic = self._create_repair_atomic(node)

        if node.type == START:
            atomic = self._create_start_atomic(node)
            is_start = True
    
        if node.type == TRANSPORT:
            atomic = self._create_transport_atomic(node)

        if node.type == TEST:
            atomic = self._create_verification_atomic(node)

        self._atomic_network.add_atomic(atomic)
        if is_start:
            self._atomic_network.mark_as_start(atomic.uid)

    def _create_buffer_atomic(self, node: Node) -> BufferAtomic:
        return BufferAtomic(node.tag_id, self._seh, node.properties['name'], node.properties['capacity'])

    def _create_custom_atomic(self, node: Node) -> CustomAtomic:
        uid = node.tag_id
        name = node.properties['name']
        duration = node.properties['duration']
        cost = node.properties['cost']
        calibration_duration = node.properties['calibration_duration']
        calibration_steps = node.properties['calibration_steps']
        calibration_cost = node.properties['calibration_cost']
        output_type = node.properties['output_type']
        return CustomAtomic(uid, self._seh, name, duration, cost, calibration_duration, calibration_steps, calibration_cost, output_type)

    def _create_divergence_atomic(self, node: Node) -> DivergenceAtomic:
        return DivergenceAtomic(node.tag_id, self._seh, node.properties['name'])

    def _create_end_atomic(self, node: Node) -> EndAtomic:
        return EndAtomic(node.tag_id, self._seh, node.properties['name'])

    def _create_random_error_atomic(self, node: Node) -> RandomErrorAtomic:
        name = node.properties['name']
        error_type = node.properties['error_type']
        error_rate = node.properties['error_rate']
        return RandomErrorAtomic(node.tag_id, self._seh, name, error_type, error_rate)

    def _create_repair_atomic(self, node: Node) -> RepairAtomic:
        uid = node.tag_id
        name = node.properties['name']
        duration = node.properties['duration']
        cost = node.properties['cost']
        calibration_duration = node.properties['calibration_duration']
        calibration_steps = node.properties['calibration_steps']
        calibration_cost = node.properties['calibration_cost']
        error_type = node.properties['error_type']
        return RepairAtomic(uid, self._seh, name, duration, cost, calibration_duration, calibration_steps, calibration_cost, error_type)

    def _create_start_atomic(self, node: Node) -> StartAtomic:
        uid = node.tag_id
        name = node.properties['name']
        output_type = node.properties['output_type']
        count = node.properties['count']
        return StartAtomic(uid, self._seh, name, output_type, count)

    def _create_transport_atomic(self, node: Node) -> TransportAtomic:
        uid = node.tag_id
        name = node.properties['name']
        duration = node.properties['duration']
        cost = node.properties['cost']
        return TransportAtomic(uid, self._seh, name, duration, cost)

    def _create_verification_atomic(self, node: Node) -> VerificationAtomic:
        uid = node.tag_id
        name = node.properties['name']
        duration = node.properties['duration']
        cost = node.properties['cost']
        calibration_duration = node.properties['calibration_duration']
        calibration_steps = node.properties['calibration_steps']
        calibration_cost = node.properties['calibration_cost']
        error_type = node.properties['error_type']
        test_rate = node.properties['test_rate']
        return VerificationAtomic(uid, self._seh, name, duration, cost, calibration_duration, calibration_steps, calibration_cost, error_type, test_rate)

    def _create_convergence_atomic(self, node: Node) -> ConvergenceAtomic:
        uid = node.tag_id
        name = node.properties['name']
        return ConvergenceAtomic(uid, self._seh, name)

    def load_resource_streams_from_lines(self, lines: List[Line]):
        primary_lines = [l for l in lines if l.is_from_secondary == False]
        secondary_lines = [l for l in lines if l.is_from_secondary == True]

        for line in secondary_lines:
            origin = self._atomic_network.get_atomic_by_uid(line.origin_node.tag_id)
            target = self._atomic_network.get_atomic_by_uid(line.target_node.tag_id)
            stream = ResourceStream(origin, target)
            origin.register_output_stream(stream)
            target.register_input_stream(stream)

        for line in primary_lines:
            origin = self._atomic_network.get_atomic_by_uid(line.origin_node.tag_id)
            target = self._atomic_network.get_atomic_by_uid(line.target_node.tag_id)
            stream = ResourceStream(origin, target)
            origin.register_output_stream(stream)
            target.register_input_stream(stream)

    def perform_analysis(self, project_name):
        self._seh.run_on_network(self._atomic_network)
        stats = self._atomic_network.get_stats()
        time = self._seh.time
        data = {
            'stats': stats,
            'time': time,
            'project_name': project_name
        }
        timestamp = SimulationFacade._generate_timestamp_id()
        report_namespace = project_name + '__' + timestamp
        raw_path = (self._data_path / ('tmp/raw/' + report_namespace + '.json')).resolve()
        with open(raw_path, 'w') as outfile:
            json.dump(data, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        rg = ReportGenerator(report_namespace, data)

    @staticmethod
    def _generate_timestamp_id() -> str:
        timestamp = datetime.datetime.now().timestamp()
        return timestamp.__str__()