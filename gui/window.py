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

        compiler_tab = CompilerTab(self)
        file_tab = FileTab(self, compiler_tab.options)

        tabs.add_tab(file_tab)
        tabs.add_tab(compiler_tab)

        return tabs
