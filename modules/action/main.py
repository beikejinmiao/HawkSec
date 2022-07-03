#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt6 import QtWidgets
from modules.ui.main_win import Ui_MainWindow


class MainWindow(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.window = Ui_MainWindow()
        self.window.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



