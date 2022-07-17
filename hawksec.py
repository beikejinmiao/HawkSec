#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt6 import QtWidgets
from modules.action.director import MainWindow


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
    window.show()
    sys.exit(app.exec())


