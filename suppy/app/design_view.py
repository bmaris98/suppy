import json
from pathlib import Path
from suppy.app.line import Line
from suppy.app.node import Node
from typing import Any, Dict, List
from suppy.app.window.open_existing_project_window import OpenExistingProjectWindow
from suppy.app.window.name_when_saving_window import NamWhenSavingWindow
from suppy.app.menu_bar import MenuBar
from suppy.app.visual_constants import NODE_HEIGHT, NODE_WIDTH
from suppy.app.design_canvas_controller import DesignCanvasController
import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle

from tkinter import Menu

class DesignView:

    def __init__(self):
        self._data_path = Path(__file__).parent / '../data'
        self._is_project_loaded = False
        self._project_name = ''
        self._main_window = tk.Tk()
        self._main_window.title('suppy')
        w, h = self._main_window.winfo_screenwidth(), self._main_window.winfo_screenheight()
        self._main_window.geometry("%dx%d+0+0" % (w, h))
        self._is_full_screen = False
        style = ThemedStyle(self._main_window)
        style.set_theme('arc')
        self._design_canvas_controller = None
        MenuBar(self._main_window, self)
        self._main_window.bind('<F5>', self._toggle_full_screen)
        self._main_window.bind('<Escape>', self._exit_full_screen)
        self._render_view_elements()

    def _toggle_full_screen(self, event):
        self._is_full_screen = not self._is_full_screen
        self._main_window.attributes('-fullscreen', self._is_full_screen)

    def _exit_full_screen(self, event):
        self._is_full_screen = False
        self._main_window.attributes('-fullscreen', self._is_full_screen)

    def start(self):
        self._main_window.mainloop()

    def _render_view_elements(self):
        self._attach_design_canvas()
        self._render_buttons()

    def _attach_design_canvas(self):
        self._design_canvas_controller = DesignCanvasController(self._main_window)
        self._design_canvas_controller.grid(row=0, column=0)

    def register_project_name(self, name: str) -> None:
        self._project_name = name
        self._is_project_loaded = True

    def save_handler(self):
        if not self._is_project_loaded:
            self._load_project_and_save()
        else:
            self.do_save()

    def _get_save_path(self):
        path = (self._data_path / ('projects/' + self._project_name + '.json')).resolve()
        return path

    def do_save(self):
        path = self._get_save_path()
        nodes, lines = self._design_canvas_controller.get_info()
        data = {
            'nodes': nodes,
            'lines': lines
        }
        with open(path, 'w') as outfile:
            json.dump(data, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)


    def _load_project_and_save(self):
        NamWhenSavingWindow(self._main_window, self)

    def _render_buttons(self):
        # b = ttk.Button(self._main_window, text = 'OK', command = self.callback)
        # b.grid(row=1, column=0)
        pass

    def _load_existing_project(self):
        OpenExistingProjectWindow(self._main_window, self)

    def _do_load_project(self, name, nodes: List[Node], lines: List[Dict[str, Any]]):
        self._project_name = name
        self._is_project_loaded = True
        self._attach_design_canvas()
        self._design_canvas_controller.load_project(nodes, lines)