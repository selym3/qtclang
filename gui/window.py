from PyQt5.QtWidgets import QMainWindow
from .tab_manager import TabManager 

from .tabs import *

class Window(QMainWindow): 
    
    def __init__(self):
        super().__init__()

        # Setup window options
        self.setWindowTitle("qtclang")

        # Create a tab manager
        self.tabs = self.create_tab_manager()

        # Format tab manager
        self.setCentralWidget(self.tabs)

    def create_tab_manager(self):

        tabs = TabManager(self)

        tabs.add_tab(FileTab(self))
        tabs.add_tab(CompilerTab(self))

        return tabs
