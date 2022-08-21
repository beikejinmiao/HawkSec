#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QPixmap, QPalette, QColor, QCursor
from PyQt6.QtWidgets import QWidget, QSizePolicy
from conf.paths import PRIVATE_RESOURCE_HOME, IMAGE_HOME
from utils.filedir import StyleSheetHelper
from modules.gui.ui_settings import Ui_Form


class SettingsWindow(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #
        self.__init_ui()
        self.__init_state()

    def __init_ui(self):
        QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.closeBtnLabel.setText('')
        #
        win_sheet = StyleSheetHelper.load_qss(name='settings').replace('IMAGE_HOME', IMAGE_HOME)
        self.setStyleSheet(win_sheet)
        # 设置PlaceholderText样式(必须在setStyleSheet后设置)
        for text_edit in [self.whiteDomTextEdit, self.whiteFileTextEdit]:
            palette = text_edit.palette()
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 100))
            text_edit.setPalette(palette)
        #
        for button in [self.closeBtnLabel, self.importDomLabel, self.importFileLabel,
                       self.checkWhiteDomBtn, self.checkWhiteFileBtn, self.builtinAlexaEnableBox,
                       self.timeoutComboBox, self.saveBtn, self.cancelBtn]:
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def __init_state(self):
        self.closeBtnLabel.clicked.connect(self.close)
        self.cancelBtn.clicked.connect(self.close)

