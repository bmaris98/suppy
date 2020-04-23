from suppy.app.visual_constants import NODE_HEIGHT, NODE_WIDTH
from suppy.app.design_canvas_controller import DesignCanvasController
import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle

class DesignView:

    def __init__(self):
        self._main_window = tk.Tk()
        self._main_window.attributes('-fullscreen', True)
        self._is_full_screen = False
        style = ThemedStyle(self._main_window)
        style.set_theme('arc')
        self._design_canvas_controller = None
        self._render_view_elements()

        self._main_window.bind('<F5>', self._toggle_full_screen)
        self._main_window.bind('<Escape>', self._exit_full_screen)

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

    def _render_buttons(self):
        # b = ttk.Button(self._main_window, text = 'OK', command = self.callback)
        # b.grid(row=1, column=0)
        pass
