#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QColor, QCursor, QPixmap
from PyQt6.QtWidgets import QDialog, QGraphicsDropShadowEffect, QSizePolicy
from conf.paths import PRIVATE_RESOURCE_HOME, IMAGE_HOME
from utils.filedir import StyleSheetHelper
from modules.gui.ui_msgbox import Ui_Dialog


class MessageBoxWindow(Ui_Dialog, QDialog):
    def __init__(self, message, level='info'):
        super().__init__()
        self.setupUi(self)
        #
        self._icon_paths = {
            'info': 'icon/msgbox_information.png',
            'warn': 'icon/msgbox_warning.png',
            'question': 'icon/msgbox_question.png',
        }
        if level not in self._icon_paths:
            level = 'info'
        self.icon_path = self._icon_paths[level]
        self.message = message
        #
        self.__init_ui()
        self.__init_state()

    def __init_ui(self):
        QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)           # 隐藏边框
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 设置窗口背景透明
        self.msgLabel.setText(self.message)
        self.closeBtnLabel.setText('')
        #
        self.iconLabel.setPixmap(QPixmap('image:%s' % self.icon_path))
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        #
        win_sheet = StyleSheetHelper.load_qss(name='msgbox').replace('IMAGE_HOME', IMAGE_HOME)
        self.setStyleSheet(win_sheet)
        #
        for button in [self.closeBtnLabel, self.okBtn, self.cancelBtn]:
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # 窗体自定义阴影
        self.render_shadow()

    def __init_state(self):
        self.closeBtnLabel.clicked.connect(self.close)
        self.okBtn.clicked.connect(self.accept)
        self.cancelBtn.clicked.connect(self.reject)

    def render_shadow(self):
        """
        https://blog.csdn.net/mahuatengmmp/article/details/113772969
        """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)  # 偏移
        shadow.setBlurRadius(12)  # 阴影半径
        shadow.setColor(QColor(128, 128, 255))  # 阴影颜色
        self.centralWidget.setGraphicsEffect(shadow)  # 将设置套用到widget窗口中


class QInfoMessageBox(MessageBoxWindow):
    def __init__(self, message, level='info'):
        super().__init__(message, level=level)
        self.cancelBtn.hide()


class QWarnMessageBox(MessageBoxWindow):
    def __init__(self, message, level='warn'):
        super().__init__(message, level=level)


class QuestionMessageBox(MessageBoxWindow):
    def __init__(self, message, level='question'):
        super().__init__(message, level=level)

