from suppy.app.line import Line
from suppy.utils.stats_constants import BUFFER, CONVERGENCE, CUSTOM, DIVERGENCE, END, RANDOM_ERROR, REPAIR, START, TEST, TRANSPORT
from suppy.app.image_loader import ImageLoader, PORT1, PORT1ERR, PORT1OK, PORTN
from tkinter.constants import LAST, LEFT, NE, NO, NW
from suppy.app.node import Node
from suppy.app.visual_constants import DOUBLE_CLICK, HOLD_LEFT_CLICK, LEFT_CLICK, MASTER_CANVAS_BACKGROUND_COLOR, MASTER_CANVAS_HEIGHT, MASTER_CANVAS_WIDTH, NODE_HEIGHT, NODE_WIDTH, RELEASE_LEFT_CLICK
import tkinter.ttk as ttk
import datetime
from typing import Any, Dict, List, Tuple
from suppy.app.position import Position
from tkinter import Canvas, Frame, Menu
from tkinter import messagebox

class DesignCanvasController(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self._image_loader = ImageLoader()
        self._node_insertion_position = Position(100, 100)
        self._node_count = 0
        self._is_dragging_node: bool = False
        self._last_dragging_position: Position
        self._nodes: List[Node] = []
        self._right_click_position = Position(0, 0) 

        self.canvas = Canvas(self, width=MASTER_CANVAS_WIDTH, height=MASTER_CANVAS_HEIGHT, background=MASTER_CANVAS_BACKGROUND_COLOR)
        self.xsb = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.ysb = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,1000,1000))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)

        self._popup_menu = self._get_popup_menu()
        self.canvas.bind('<Button-3>', self.open_canvas_menu)
        self._is_drawing_line = False
        self._current_drawing_line = None
        self._current_drawing_line_start: Tuple[int, int]
        self._drawing_args: Dict[str, Any] = {}
        self.canvas.bind('<Motion>', self._handle_canvas_motion)
        self.lines: List[Line] = []
        self.messagebox = None
        self._bind_line_double_click()

    def open_canvas_menu(self, event):
        self._right_click_position = Position(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        try:
            self._popup_menu.tk_popup(event.x_root, event.y_root, '')
        finally:
            self._popup_menu.grab_release()
    
    def _bind_line_double_click(self):
        self.canvas.tag_bind('line', DOUBLE_CLICK, lambda event: self._delete_line(event))

    def _delete_line(self, event):
        view_id = event.widget.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))[0]
        self.lines = [line for line in self.lines if not line.view_id == view_id]
        self.canvas.delete(view_id)

    def _get_popup_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label='Add Start', command=self._add_prompt_start)
        menu.add_command(label='Add Transform', command=self._add_prompt_custom)
        menu.add_command(label='Add Transport', command=self._add_prompt_transport)
        menu.add_command(label='Add Buffer', command=self._add_prompt_buffer)
        menu.add_command(label='Add Confluence', command=self._add_prompt_convergence)
        menu.add_command(label='Add Divergence', command=self._add_prompt_divergence)
        menu.add_command(label='Add Verification', command=self._add_prompt_verification)
        menu.add_command(label='Add Repair', command=self._add_prompt_repair)
        menu.add_command(label='Add Error Generator', command=self._add_prompt_error)
        menu.add_command(label='Add End', command=self._add_prompt_end)
        return menu

    def _add_prompt_start(self):
        node = self._create_base_node()
        node.type = START
        node.has_input_port = False
        self._attach_node_to_canvas(node)

    def _create_base_node(self) -> Node:
        node = Node()
        node.tag_id = self._generate_timestamp_id()
        node.has_output_port = True
        node.has_input_port = True
        x, y = self._right_click_position.value
        node.position = Position(x, y)
        return node

    def _add_prompt_end(self):
        node = self._create_base_node()
        node.type = END
        node.has_output_port = False
        self._attach_node_to_canvas(node)

    def _add_prompt_custom(self):
        node = self._create_base_node()
        node.type = CUSTOM
        node.multiple_inputs = True
        self._attach_node_to_canvas(node)

    def _add_prompt_transport(self):
        node = self._create_base_node()
        node.type = TRANSPORT
        self._attach_node_to_canvas(node)

    def _add_prompt_buffer(self):
        node = self._create_base_node()
        node.type = BUFFER
        self._attach_node_to_canvas(node)

    def _add_prompt_verification(self):
        node = self._create_base_node()
        node.type = TEST
        self._attach_node_to_canvas(node)

    def _add_prompt_convergence(self):
        node = self._create_base_node()
        node.type = CONVERGENCE
        node.multiple_inputs = True
        self._attach_node_to_canvas(node)

    def _add_prompt_repair(self):
        node = self._create_base_node()
        node.type = REPAIR
        self._attach_node_to_canvas(node)

    def _add_prompt_error(self):
        node = self._create_base_node()
        node.type = RANDOM_ERROR
        self._attach_node_to_canvas(node)

    def _add_prompt_divergence(self):
        node = self._create_base_node()
        node.type = DIVERGENCE
        node.multiple_outputs = True
        self._attach_node_to_canvas(node)

    def move_start(self, event):
        if not self._is_dragging_node:
            self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        if not self._is_dragging_node:
            self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _attach_node_to_canvas(self, node: Node) -> None:
        x, y = node.position.value
        image = self._image_loader.get_image(node.type)

        node_id: int = self.canvas.create_image(x, y, image=image, anchor=NW, tags=node.tag_id)
        node.view_id = str(node_id)
        self._add_input_ports(node)
        self._add_output_ports(node)
        self._nodes.append(node)
        self._bind_default_listeners_to_node(node)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def _add_input_ports(self, node: Node):
        x, y = node.position.value
        if node.has_input_port:
            if node.multiple_inputs:
                image = self._image_loader.get_image(PORTN)
            else:
                image = self._image_loader.get_image(PORT1)
            port_id = node.tag_id + 'in'
            node.input_id = self.canvas.create_image(x, y+int(NODE_HEIGHT/3), image=image, anchor=NE, tags = port_id)

    def _get_port_width_height(self):
        return int(NODE_WIDTH/3), int(NODE_HEIGHT)/3

    def _add_output_ports(self, node: Node):
        x, y = node.position.value
        if node.type == TEST:
            self._add_output_ports_for_test_stand(node)
            return
        if node.has_output_port:
            if node.multiple_outputs:
                image = self._image_loader.get_image(PORTN)
            else:
                image = self._image_loader.get_image(PORT1)
            port_id = node.tag_id + 'out'
            node.output_id = self.canvas.create_image(x+int(4*NODE_WIDTH/3), y+int(NODE_HEIGHT/3), image=image, anchor=NE, tags = port_id)
    
    def _add_output_ports_for_test_stand(self, node: Node):
        x, y = node.position.value
        image_ok = self._image_loader.get_image(PORT1OK)
        image_err = self._image_loader.get_image(PORT1ERR)
        port_id_ok = node.tag_id + 'out'
        port_id_err = node.tag_id + 'out_err'
        node.output_id = self.canvas.create_image(x+int(4*NODE_WIDTH/3), y, image=image_ok, anchor=NE, tags=port_id_ok)
        node.secondary_output_id = self.canvas.create_image(x+int(4*NODE_WIDTH/3), y+int(2*NODE_HEIGHT/3), image=image_err, anchor=NE, tags=port_id_err)
    

    def _generate_node_id(self) -> str:
        self._node_count += 1
        return self._node_count.__str__()

    @staticmethod
    def _generate_timestamp_id() -> str:
        timestamp = datetime.datetime.now().timestamp()
        return timestamp.__str__()

    def _bind_default_listeners_to_node(self, node: Node) -> None:
        self.canvas.tag_bind(node.tag_id, HOLD_LEFT_CLICK, lambda event: self._handle_node_left_click_hold(event, node))
        self.canvas.tag_bind(node.tag_id, RELEASE_LEFT_CLICK, lambda event: self._handle_node_left_click_release(event))
        
        if node.has_output_port:
            if node.type == TEST:
                self.canvas.tag_bind(node.tag_id + 'out_err', LEFT_CLICK, lambda event: self._handle_output_left_click(event, node, True))
            self.canvas.tag_bind(node.tag_id + 'out', LEFT_CLICK, lambda event: self._handle_output_left_click(event, node, False))
        
        if node.has_input_port:
            self.canvas.tag_bind(node.tag_id + 'in', LEFT_CLICK, lambda event: self._handle_input_left_click(event, node))

    def _handle_input_left_click(self, event, node):
        if self._current_drawing_line == None:
            return
        if node.tag_id == self._drawing_args['node'].tag_id:
            self._delete_active_line_drawing()
            return
        port_id = event.widget.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))[0]

        if not self._can_draw_another_input(port_id, node):
            self._delete_active_line_drawing()
            messagebox.showerror('Port full', 'Input port already has a connection.')
            return

        middle_x, middle_y = self._get_port_middle(port_id)
        sx, sy = self._current_drawing_line_start
        line_id = self._draw_line(sx, sy, middle_x, middle_y, False)
        self._current_drawing_line = None
        self._attach_line(self._drawing_args['node'].tag_id, node.tag_id, self._drawing_args['is_secondary'], line_id)
        self._drawing_args = {}

    def _can_draw_another_input(self, port_id: int, node: Node) -> bool:
        if not node.multiple_inputs:
            return not self._port_has_line(port_id)
        return True


    def _attach_line(self, origin, target, is_secondary, view_id, override = False):
        line = Line()
        self.canvas.delete(view_id)
        line.origin_node = self._get_node_by_tag_id(origin)
        line.target_node = self._get_node_by_tag_id(target)
        line.is_from_secondary = is_secondary
        output_id = line.origin_node.output_id
        if is_secondary:
            output_id = line.origin_node.secondary_output_id
        line.origin_port_id = output_id
        line.target_port_id = line.target_node.input_id
        x1, y1 = self._get_port_middle(line.origin_port_id)
        x2, y2 = self._get_port_middle(line.target_port_id)
        line.view_id = self._draw_line(x1, y1, x2, y2)
        if override == False:
            self.lines.append(line)

    def _get_port_middle(self, port_id: int) -> Tuple[int, int]:
        coords = self.canvas.coords(port_id)
        x = coords[0]
        y = coords[1]
        width, height = self._get_port_width_height()
        middle_x, middle_y = x - int(width/2), y + int(height/2) + 3
        return middle_x, middle_y

    def _get_node_by_tag_id(self, tag_id: str):
        for node in self._nodes:
            if node.tag_id == tag_id:
                return node
        return Node()

    def _handle_output_left_click(self, event, node, is_secondary):
        # clean line if already drawing mode
        if not self._current_drawing_line == None:
            self._delete_active_line_drawing()
            return

        self._delete_active_line_drawing()
        port_id = event.widget.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))[0]
        
        if not self._can_draw_another_output(port_id, node):
            messagebox.showerror('Port full', 'Output port already has a connection.')
            return
        
        self._drawing_args['node'] = node
        self._drawing_args['output'] = port_id
        self._drawing_args['is_secondary'] = is_secondary
        mouse_x = self.canvas.winfo_pointerx()
        mouse_y = self.canvas.winfo_pointery()
        cx = self.canvas.canvasx(mouse_x)
        cy = self.canvas.canvasy(mouse_y)
        middle_x, middle_y = self._get_port_middle(port_id)
        self._current_drawing_line_start = (middle_x, middle_y)
        self._draw_line(middle_x, middle_y, cx , cy, True)
        
    def _can_draw_another_output(self, port_id: int, node: Node) -> bool:
        if port_id == node.secondary_output_id:
            return not self._port_has_line(port_id)
        if not node.multiple_outputs:
            return not self._port_has_line(port_id)
        return True

    def _port_has_line(self, port_id: int) -> bool:
        for line in self.lines:
            if line.origin_port_id == port_id or line.target_port_id == port_id:
                return True
        return False

    def _handle_canvas_motion(self, event):
        if self._current_drawing_line == None:
            return
        mouse_x = self.canvas.winfo_pointerx()
        mouse_y = self.canvas.winfo_pointery()
        cx = self.canvas.canvasx(mouse_x)
        cy = self.canvas.canvasy(mouse_y)
        self.canvas.delete(self._current_drawing_line)
        start_x, start_y = self._current_drawing_line_start
        dx = 1
        dy = 1
        if start_x > cx:
            dx = -1
        if start_y > cy:
            dy = -1 
        self._draw_line(start_x, start_y, cx - dx, cy - dy, True)

    def _draw_line(self, start_x, start_y, end_x, end_y, motion=False) -> int:
        self._delete_active_line_drawing()
        id = self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=LAST, width=3, tags='line')
        if motion:
            self._current_drawing_line = id
        return id

    def _delete_active_line_drawing(self):
        if self._current_drawing_line == None:
            return
        self.canvas.delete(self._current_drawing_line)
        self._current_drawing_line = None
        

    # fix event typing here, double check misc class
    def _handle_node_left_click_hold(self, event, node: Node) -> None:
        if not self._current_drawing_line == None:
            return
        ex = event.x
        ey = event.y
        if not self._is_dragging_node:
            self._is_dragging_node = True
            self._last_dragging_position = Position(ex, ey)
            return

        last_x, last_y = self._last_dragging_position.value
        delta_x = ex - last_x
        delta_y = ey - last_y
        
        self._last_dragging_position = Position(ex, ey)
        self.canvas.move(node.view_id, delta_x, delta_y)
        if node.has_output_port:
            self.canvas.move(node.output_id, delta_x, delta_y)
        if node.has_input_port:
            self.canvas.move(node.input_id, delta_x, delta_y)
        if not node.secondary_output_id == -1:
            self.canvas.move(node.secondary_output_id, delta_x, delta_y)

        self._move_lines(node)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def _handle_node_left_click_release(self, event) -> None:
        self._is_dragging_node = False
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def _move_lines(self, node):
        inputs = self._get_input_lines(node)
        outputs = self._get_output_lines(node)
        lines = []
        lines.extend(inputs)
        lines.extend(outputs)
        self._redraw_lines(lines)

    def _get_output_lines(self, node: Node) -> List[Line]:
        lines = []
        for line in self.lines:
            if line.origin_node.tag_id == node.tag_id:
                lines.append(line)
        return lines

    def _get_input_lines(self, node: Node) -> List[Line]:
        lines = []
        for line in self.lines:
            if line.target_node.tag_id == node.tag_id:
                lines.append(line)
        return lines

    def _redraw_lines(self, lines: List[Line]) -> None:
        for line in lines:
            x1, y1 = self._get_port_middle(line.origin_port_id)
            x2, y2 = self._get_port_middle(line.target_port_id)
            self.canvas.delete(line.view_id)
            line_view_id = self._draw_line(x1, y1, x2, y2)
            line.view_id = line_view_id

    def _get_node_with_output_id(self, port_id: int):
        for node in self._nodes:
            if node.output_id == port_id:
                return node
            elif node.secondary_output_id == port_id:
                return node