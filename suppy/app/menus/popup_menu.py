from tkinter import Listbox, Menu
from typing import Callable, List, Tuple


class PopupMenu(Listbox):

    def __init__(self, target, commands: List[Tuple[str, Callable]]):
        self.menu = Menu(self, tearoff=0)
        for label, action in commands:
            self.menu.add_command(label=label, command=action)