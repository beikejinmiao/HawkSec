#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt6.QtWidgets import QLineEdit, QWidget
from PyQt6.QtCore import pyqtSignal


class QTimeLineEdit(QLineEdit):
    calendar_focus_in = pyqtSignal()
    calendar_focus_out = pyqtSignal()

    def focusInEvent(self, e):
        self.calendar_focus_in.emit()
        super().focusInEvent(e)

    def focusOutEvent(self, e):
        self.calendar_focus_out.emit()
        super().focusOutEvent(e)


class QNotClickWidget(QWidget):
    def mousePressEvent(self, event):
        pass
