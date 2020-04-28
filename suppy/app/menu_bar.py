import tkinter
  
class MenuBar:
    def __init__(self, window):
        # Create and display the main menu bar
        menuBar = tkinter.Menu(window)
  
        # Create a pull-down menu for file operations
        fileMenu = tkinter.Menu(menuBar, tearoff = False)
        fileMenu.add_command(label = "New Project")
        fileMenu.add_command(label = "Project from example")
        fileMenu.add_command(label = "Open existing project")
        menuBar.add_cascade(menu = fileMenu, label = "Project")
        menuBar.add_command(label = "Save")
        menuBar.add_command(label = "Run")
        window.config(menu=menuBar)