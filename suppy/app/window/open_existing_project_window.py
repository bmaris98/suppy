from typing import Any, Dict, List, Tuple
from suppy.app.line import Line
from suppy.app.position import Position
from suppy.app.node import Node
import tkinter as tk
import tkinter.ttk as ttk
import glob
import json
from pathlib import Path
from tkinter import messagebox
from tkinter.constants import E, N, S, W
from ttkthemes import ThemedStyle

class OpenExistingProjectWindow:

    def __init__(self, root, window_controller):
        self.window_controller = window_controller
        self.window = tk.Toplevel(root)
        self.window.title('Open Project')
        self.variable = tk.StringVar(self.window)
        self.select_a_value = 'Select a project'
        style = ThemedStyle(self.window)
        style.set_theme('arc')

        label = ttk.Label(self.window, text='Please select a project to open.')
        label.grid(row=0, columnspan=2, pady=7)

        all_projects = glob.glob('suppy/data/projects/*.json')
        all_projects = [p.split('\\')[1][0:-5] for p in all_projects]
        all_projects.insert(0, self.select_a_value)

        self.opt = ttk.OptionMenu(self.window, self.variable, *all_projects)
        self.opt.grid(row=1, columnspan=2, padx=10, pady=10)

        load_button = ttk.Button(self.window, text="Load", command=self._load)
        load_button.grid(row=2, column=0, columnspan=1, sticky=E, padx=5, pady=5)

        cancel_button = ttk.Button(self.window, text="Cancel", command=self._quit)
        cancel_button.grid(row=2, column=1, columnspan=1, sticky=W, padx=5, pady=5)

    def _quit(self):
        self.window.destroy()

    def _load(self):
        text = self.variable.get()
        if text == self.select_a_value:
            messagebox.showerror('No project', 'You need to select a project to be loaded.')
            return
        path = (Path(__file__).parent / ('../../data/projects/' + text + '.json')).resolve()
        data = ''
        with open(path) as f:
            data = json.load(f)

        nodes, lines = self._parse_data(data)

        self.window_controller._do_load_project(text, nodes, lines)
        self._quit()

    def _parse_data(self, data) -> Tuple[List[Node], List[Dict[str, Any]]]:
        nodes = []
        lines = []
        for node in data['nodes']:
            new = Node()
            new.tag_id = node['tag_id']
            new.type = node['type']
            new.properties = node['properties']
            x = node['position']['_x']
            y = node['position']['_y']
            new.position = Position(x, y)
            new.has_input_port = node['has_input_port']
            new.has_output_port = node['has_output_port']
            new.multiple_inputs = node['multiple_inputs']
            new.multiple_outputs = node['multiple_outputs']
            nodes.append(new)

        for line in data['lines']:
            new = {}
            new['is_from_secondary'] = line['is_from_secondary']
            new['origin_node'] = line['origin_node']['tag_id']
            new['target_node'] = line['target_node']['tag_id']
            lines.append(new)

        return nodes, lines
