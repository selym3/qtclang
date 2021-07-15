from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout

class TabManager(QWidget):

    def __init__(self, parent): 
        super().__init__(parent)

        # Create manager layout
        self.layout = QVBoxLayout(self)        

        # Create tab manager
        self.tabs = QTabWidget()

        # Create layout for tabs
        self.tabs_layout = QVBoxLayout(self.tabs)
        self.tabs.setLayout(self.tabs_layout)

        # Setup layouts
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def add_tab(self, name, widget):
        self.tabs.addTab(name, widget)