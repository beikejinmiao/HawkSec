#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from modules.win.start import SplashScreen


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.setMinimumSize(960, 680)
    splash.show()
    sys.exit(app.exec())

