#!/usr/bin/python

import sys

from PyQt5.QtWidgets import QApplication
from gui import Window

if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    w, h = 480, 640
    win.setMinimumSize(w, h)

    win.show()

    sys.exit(app.exec_())
