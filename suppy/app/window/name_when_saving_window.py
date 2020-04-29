import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.constants import E, N, S, W
from ttkthemes import ThemedStyle


class NamWhenSavingWindow:

    def __init__(self, root, window_controller):
        self.window_controller = window_controller
        self.window = tk.Toplevel(root)
        self.window.title('Save')
        style = ThemedStyle(self.window)
        style.set_theme('arc')
        label = ttk.Label(self.window, text='Please enter the name of the project.')
        label.grid(row=0, columnspan=2, pady=5)

        self.entry = ttk.Entry(self.window, width=50)
        self.entry.grid(row=1, columnspan=2, padx=10, pady=10)

        save_button = ttk.Button(self.window, text="Save", command=self._save)
        save_button.grid(row=2, column=0, columnspan=1, sticky=E)

        cancel_button = ttk.Button(self.window, text="Cancel", command=self._quit)
        cancel_button.grid(row=2, column=1, columnspan=1, sticky=W)

    def _quit(self):
        self.window.destroy()

    def _save(self):
        text = self.entry.get()
        if text == '':
            messagebox.showerror('Invalid Input', 'Project name can not be empty.')
            return
        self.window_controller.register_project_name(text)
        self.window_controller.save_handler()
        self._quit()
