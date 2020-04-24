from suppy.app.position import Position
from typing import Any, Dict


class Node:

    def __init__(self):
        self.view_id: str
        self.tag_id: str
        self.type: str = 'default'
        self.properties: Dict[str, Any] = {}
        self.position: Position
        self.has_input_port: bool = False
        self.has_output_port: bool = False
        self.multiple_inputs: bool = False
        self.multiple_outputs: bool = False
        self.input_id: int = -1
        self.output_id: int = -1
        self.secondary_output_id: int = -1