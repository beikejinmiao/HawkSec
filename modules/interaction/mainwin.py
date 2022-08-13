#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox, QSizePolicy, QLayout
from PyQt6.QtCore import QThread
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QColor
from modules.gui.ui_main_window import Ui_MainWindow as UiMainWindow
from conf.paths import PRIVATE_RESOURCE_HOME, IMAGE_HOME
from pathlib import Path, PurePosixPath
from utils.filedir import StyleSheetHelper

IMAGE_HOME = Path(IMAGE_HOME).as_posix()


class MainWindow(UiMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__init_gui()
        self.__init_state()

    def __init_gui(self):
        QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
        # StyleSheet中文件路径必须使用posix格式
        # https://stackoverflow.com/questions/51750501/do-not-insert-a-background-picture-into-widget-setstylesheet
        bg_pic_path = Path(os.path.join(IMAGE_HOME, 'bg.png')).as_posix()
        self.centralwidget.setStyleSheet('#centralwidget {border-image: url(%s);}' % bg_pic_path)
        # 使用border-image而不是background-image会让图片自适应widget大小
        # self.centralwidget.setStyleSheet(
        #     '#centralwidget {background-image: url(%s); background-repeat: no-repeat}' % bg_pic_path)

        self.logoLabel.setPixmap(QPixmap("image:logo.png"))
        # https://stackoverflow.com/questions/5653114/display-image-in-qt-to-fit-label-size
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.robotLabel.setPixmap(QPixmap("image:robot.png"))
        self.robotLabel.setScaledContents(True)
        self.robotLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.helpLabel.setPixmap(QPixmap("image:icon/help.png"))
        self.helpLabel.setScaledContents(True)
        self.helpLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.settingLabel.setPixmap(QPixmap("image:icon/setting.png"))
        self.settingLabel.setScaledContents(True)
        self.settingLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        # 设置PlaceholderText字体颜色和透明度
        self.line_edits = (self.addressLineEdit, self.portLineEdit,
                           self.userLineEdit, self.passwdLineEdit, self.pathLineEdit)
        for line_edit in self.line_edits:
            palette = line_edit.palette()
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 100))
            line_edit.setPalette(palette)

        win_sheet = StyleSheetHelper.main_win().replace('IMAGE_HOME', IMAGE_HOME)
        self.setStyleSheet(win_sheet)

    def __init_state(self):
        # 保证Layout隐藏部分组件时,剩余组件能自动移动填充(例如grid layout隐藏前两行,后几行能自动上移)
        # https://stackoverflow.com/questions/2293708/pyqt4-hide-widget-and-resize-window
        self.dynGridLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        #
        self.__toggle_sftp()
        self.httpRadioBtn.clicked.connect(lambda: self.__toggle_sftp(visible=False))
        self.httpsRadioBtn.clicked.connect(lambda: self.__toggle_sftp(visible=False))
        self.sftpRadioBtn.clicked.connect(lambda: self.__toggle_sftp(visible=True))

    def __toggle_sftp(self, visible=False):
        sftp_edits = (self.portLineEdit, self.userLineEdit, self.passwdLineEdit, self.pathLineEdit)
        for line_edit in sftp_edits:
            line_edit.setVisible(visible)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
