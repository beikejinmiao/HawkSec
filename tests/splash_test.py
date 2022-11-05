#!/usr/bin/env python  
# -*- coding:utf-8 -*-
import os
import sys
import time
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QTextBrowser, QLineEdit, QVBoxLayout, QSplashScreen, QProgressBar
from conf.paths import PRIVATE_RESOURCE_HOME

"""
使用默认QSplashScreen
https://gist.github.com/345161974/8897f9230006d51803c987122b3d4f17

自定义实现SplashScreen
https://learndataanalysis.org/source-code-create-a-modern-style-flash-screen-pyqt5-tutorial/
"""


class Form(QDialog):
    """ Just a simple dialog with a couple of widgets
    """

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.setWindowTitle('Just a dialog')
        self.lineEdit = QLineEdit("Write something and press Enter")
        self.lineEdit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)
        self.lineEdit.setFocus()

    def update_ui(self):
        self.browser.append(self.lineEdit.text())


if __name__ == "__main__":
    QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QPixmap("image:bg.png")

    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
    splash.setEnabled(False)
    # splash = QSplashScreen(splash_pix)
    # adding progress bar
    progressBar = QProgressBar(splash)
    progressBar.setMaximum(10)
    progressBar.setGeometry(0, splash_pix.height() - 50, splash_pix.width(), 20)

    # splash.setMask(splash_pix.mask())

    splash.show()
    splash.showMessage("<h1><font color='green'>Welcome BeeMan!</font></h1>", Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.black)

    for i in range(1, 11):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    # Simulate something that takes time
    time.sleep(1)

    form = Form()
    form.show()
    splash.finish(form)
    sys.exit(app.exec())



