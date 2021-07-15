from PyQt5.QtWidgets import QMainWindow
from .tab_manager import TabManager 

class Window(QMainWindow): 
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qtclang")

        self.tabs = TabManager(self)
        self.setCentralWidget(self.tabs)
