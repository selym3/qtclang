from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Tab(QScrollArea):

    def __init__(self, parent, name):
        super().__init__(parent)

        self.name = name

        self.root = QGroupBox()
        self.form = QFormLayout()
        self.root.setLayout(self.form)

        self.setWidget(self.root)
        self.setWidgetResizable(True)
    
    def addComponent(self, component):
        self.form.addRow(component)
    