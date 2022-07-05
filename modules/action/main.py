#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt6 import QtWidgets
from modules.ui.main_win import Ui_MainWindow
from modules.ui.settings import Ui_Form as SetupUiForm


class MainWindow(Ui_MainWindow, QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.window = Ui_MainWindow()
        self.window.setupUi(self)
        self.window.menuActionGeneral.triggered.connect(self.setupWindow)

    def setupWindow(self):
        self.setupUiForm = SetupUiForm()
        self.setupUiForm.setupUi(self.setupUiForm)
        self.setupUiForm.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



