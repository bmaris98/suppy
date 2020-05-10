import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.constants import E, END, N, S, W
from typing import Any, Dict, List
from ttkthemes import ThemedStyle


class UpdateNodeWindow:

    def __init__(self, root, window_controller, config: List[str], values: Dict[str, str]):
        self.config: List[str] = config
        self.values: Dict[str, str] = values
        self.result: Dict[str, Any] = {}
        self.result: Dict[str, Any] = {}
        self.window_controller = window_controller
        self.window = tk.Toplevel(root)
        self.window.title('Configure Node')
        style = ThemedStyle(self.window)
        style.set_theme('arc')
        self.current_row = 0
        self._entries = {}
        self._add_entry('Name', 'name')
        self._add_entry('Capacity', 'capacity')
        self._add_entry('Duration', 'duration')
        self._add_entry('Cost', 'cost')
        self._add_entry('Calibration Duration', 'calibration_duration')
        self._add_entry('Calibration Steps', 'calibration_steps')
        self._add_entry('Calibration Cost', 'calibration_cost')
        self._add_entry('Output Type', 'output_type')
        self._add_entry('Errpr Type', 'error_type')
        self._add_entry('Error Rate', 'error_rate')
        self._add_entry('Count', 'count')
        self._add_entry('Test Rate', 'test_rate')

        save_button = ttk.Button(self.window, text="Update", command=self._update)
        save_button.grid(row=self.current_row, column=0, columnspan=1, sticky=E)

        cancel_button = ttk.Button(self.window, text="Cancel", command=self._quit)
        cancel_button.grid(row=self.current_row, column=1, columnspan=1, sticky=W)

    def _add_entry(self, label_text, key):
        if not key in self.config:
            return
        label = ttk.Label(self.window, text=label_text)
        label.grid(row=self.current_row, columnspan=2, pady=5)
        self.current_row += 1
        entry = ttk.Entry(self.window, width=50)
        entry.grid(row=self.current_row, columnspan=2, padx=10, pady=10)
        entry.delete(0, END)
        entry.insert(0, self.values[key])
        self._entries[key] = entry
        self.current_row += 1

    def _quit(self):
        self.window.destroy()

    def _collect_data(self) -> bool:
        try:
            self._collect_string('name')
            self._collect_positive_int('capacity')
            self._collect_int('duration')
            self._collect_int('cost')
            self._collect_int('calibration_duration')
            self._collect_positive_int('calibration_steps')
            self._collect_int('calibration_cost')
            self._collect_string('output_type')
            self._collect_string('error_type')
            self._collect_error_rate()
            self._collect_positive_int('count')
            self._collect_positive_int('test_rate')
            return True
        except Exception as e:
            messagebox.showerror('Invalid Input', str(e))
            return False

    def _collect_string(self, key):
        if not key in self.config:
            return
        value = self._entries[key].get()
        if value == '':
            raise Exception('Text field can not be emtpy (' + key + ').')
        self.result[key] = value

    def _collect_positive_int(self, key):
        if not key in self.config:
            return
        value = self._entries[key].get()
        try:
            value = int(value)
        except:
            raise Exception('Invalid integer value for ' + key + '.')
        if value <= 0:
            raise Exception('Must be greater than 0 (' + key + ').')
        self.result[key] = value

    def _collect_int(self, key):
        if not key in self.config:
            return
        value = self._entries[key].get()
        try:
            value = int(value)
        except:
            raise Exception('Invalid integer value for ' + key + '.')
        if value < 0:
            raise Exception('Must be greater than or equal 0 (' + key + ').')
        self.result[key] = value

    def _collect_error_rate(self):
        key = 'error_rate'
        if not key in self.config:
            return
        value = self._entries[key].get()
        try:
            value = float(value)
        except:
            raise Exception('Invalid data type for error rate.')
        if value < 0 or value > 1:
            raise Exception('Error rate must be in the interval [0, 1].')
        self.result[key] = value

    def _update(self):
        ok = self._collect_data()
        if ok:
            self.window_controller.update_node(self.result)
            self._quit()
