import tkinter
  
class MenuBar:
    def __init__(self, window, window_controller):
        # Create and display the main menu bar
        menuBar = tkinter.Menu(window)
  
        # Create a pull-down menu for file operations
        fileMenu = tkinter.Menu(menuBar, tearoff = False)
        fileMenu.add_command(label = "New Project")
        fileMenu.add_command(label = "Open existing project", command=window_controller._load_existing_project)
        menuBar.add_cascade(menu = fileMenu, label = "Project")
        menuBar.add_command(label = "Save", command=window_controller.save_handler)
        menuBar.add_command(label = "Run")
        window.config(menu=menuBar)