from tkinter.constants import NW
from suppy.app.node import Node
from suppy.app.visual_constants import HOLD_LEFT_CLICK, MASTER_CANVAS_BACKGROUND_COLOR, MASTER_CANVAS_HEIGHT, MASTER_CANVAS_WIDTH, NODE_HEIGHT, NODE_WIDTH, RELEASE_LEFT_CLICK
import tkinter.ttk as ttk
import datetime
from typing import Dict, List
from suppy.app.position import Position
from tkinter import Canvas, Frame, Menu, PhotoImage
from pathlib import Path
from PIL import ImageTk, Image

class DesignCanvasController(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self._node_insertion_position = Position(100, 100)
        self._node_count = 0
        self._is_dragging_node: bool = False
        self._last_dragging_position: Position
        self._nodes: List[Node] = []
        self._mario = self._get_mario()
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

    def open_canvas_menu(self, event):
        self._right_click_position = Position(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        try:
            self._popup_menu.tk_popup(event.x_root, event.y_root, '')
        finally:
            self._popup_menu.grab_release()
    
    def _get_popup_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label='Add Start', command=self.add_node)
        menu.add_command(label='Add End', command=self.add_node)
        menu.add_command(label='Add Custom', command=self.add_node)
        menu.add_command(label='Add Transport', command=self.add_node)
        menu.add_command(label='Add Buffer', command=self.add_node)
        menu.add_command(label='Add Verification', command=self.add_node)
        menu.add_command(label='Add Convergence', command=self.add_node)
        menu.add_command(label='Add Repair', command=self.add_node)
        menu.add_command(label='Add Error Generator', command=self.add_node)
        return menu

    def move_start(self, event):
        if not self._is_dragging_node:
            self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        if not self._is_dragging_node:
            self.canvas.scan_dragto(event.x, event.y, gain=1)

    def add_node(self) -> None:
        self._attach_node_to_canvas(self._right_click_position)

    def _attach_node_to_canvas(self, position: Position) -> None:
        x, y = position.value
        tag_id = self._generate_node_id()
        image = self._get_mario()

        node_id: int = self.canvas.create_image(x, y, image=self._mario, anchor=NW, tags=tag_id)
        #node_id: int = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=tag_id)
        new_node = Node(node_id, tag_id)
        new_node.load_image(image)
        self._nodes.append(new_node)
        self._bind_default_listeners_to_node(new_node)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

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

    # fix event typing here, double check misc class
    def _handle_node_left_click_hold(self, event, node: Node) -> None:
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
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def _handle_node_left_click_release(self, event) -> None:
        self._is_dragging_node = False
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def _get_mario(self):
        img = Image.open(self._get_path())
        img = img.resize((NODE_WIDTH, NODE_HEIGHT))
        return ImageTk.PhotoImage(img)

    def _get_path(self):
        base_path = Path(__file__).parent
        file_path = (base_path / '../data/assets/mario.png').resolve()
        return file_path