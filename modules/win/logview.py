#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QColor
from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from conf.paths import IMAGE_HOME
from utils.filedir import StyleSheetHelper
from modules.gui.ui_logview import Ui_Form
from libs.logger import QLogTailReader


class LogViewWindow(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #
        self.log_reader = QLogTailReader()
        self.log_reader.start()
        #
        self.__init_ui()
        self.__init_state()

    def __init_ui(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)           # 隐藏边框
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 设置窗口背景透明
        self.closeBtnLabel.setText('')
        #
        win_sheet = StyleSheetHelper.load_qss(name='logview').replace('IMAGE_HOME', IMAGE_HOME)
        self.setStyleSheet(win_sheet)
        #
        self.closeBtnLabel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # 窗体自定义阴影
        self.render_shadow()

    def __init_state(self):
        self.cancelBtn.clicked.connect(self.close)
        self.clearBtn.clicked.connect(lambda: self.logTextEdit.setPlainText(''))
        self.closeBtnLabel.clicked.connect(self.close)
        self.log_reader.readline.connect(lambda line: self.logTextEdit.appendPlainText(line))

    def render_shadow(self):
        """
        https://blog.csdn.net/mahuatengmmp/article/details/113772969
        """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)  # 偏移
        shadow.setBlurRadius(12)  # 阴影半径
        shadow.setColor(QColor(128, 128, 255))  # 阴影颜色
        self.centralWidget.setGraphicsEffect(shadow)  # 将设置套用到widget窗口中

