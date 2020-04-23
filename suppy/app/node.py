from suppy.app.position import Position
from typing import Any, Dict


class Node:

    def __init__(self, view_id: int, tag_id: str):
        self._view_id = view_id
        self._tag_id = tag_id
        self._type: str
        self._properties: Dict[str, Any] = {}
        self._position: Position
        self._input_ports_count: int
        self._output_ports_count: int
        self._image = None

    @property
    def view_id(self):
        return self._view_id

    @property
    def tag_id(self):
        return self._tag_id

    def load_image(self, image):
        self._image = image