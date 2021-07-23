from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Component(QGroupBox):
    
    def __init__(self, name):
        super().__init__(name)

        self.form = QFormLayout()
        self.setLayout(self.form)

    def addWidgets(self, *widgets):
        self.form.addRow(*widgets)