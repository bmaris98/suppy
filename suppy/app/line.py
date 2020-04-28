from suppy.app.node import Node


class Line:

    def __init__(self):
        self.view_id: int
        self.origin_node: Node
        self.target_node: Node
        self.origin_port_id: int
        self.target_port_id: int
        self.is_from_secondary: bool = False