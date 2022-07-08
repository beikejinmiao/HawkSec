#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt6 import QtWidgets
from modules.ui.main_win import Ui_MainWindow as UiMainWindow
from modules.ui.settings import Ui_Form as UiSettingForm


class SettingWindow(UiSettingForm, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.uiSetupForm = UiSettingForm()
        self.setupUi(self)


class MainWindow(UiMainWindow, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settingWindow = SettingWindow()
        self.menuActionGeneral.triggered.connect(self.settingWindow.show)
        #
        self.connect()

    def connect(self):
        self.startBtn.clicked.connect(self.start)

    def start(self):
        mtarget = self.monitTarget.text()
        protocol = self.monitProtoComboBox.currentText()
        mtype = self.monitTypeComboBox.currentIndex()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



