#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
from PyQt5.QtWidgets import QLineEdit, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QRect
from PyQt5.QtGui import QColor, QPainter, QPixmap
from utils.filedir import StyleSheetHelper
from libs.enums import QMSG_BOX_REPLY_YES, QMSG_BOX_REPLY_NO


class QClickLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


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


class QAbstractMessageBox(object):
    def __init__(self, parent: QWidget, text: str, icon: str):
        self.msgbox = QMessageBox(parent)
        self.msgbox.setText(text)
        self.msgbox.setWindowTitle('提示')
        self.msgbox.setIconPixmap(QPixmap('image:%s' % icon))
        self.msgbox.setStyleSheet(StyleSheetHelper.load_qss(name='msgbox'))

    def show(self):
        self.msgbox.exec()
        return QMSG_BOX_REPLY_YES


class QInfoMessageBox(QAbstractMessageBox):
    def __init__(self, parent: QWidget, text: str):
        super().__init__(parent, text, 'icon/msgbox_information.png')
        # self.msgbox.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msgbox.addButton(parent.tr('确认'), QMessageBox.ButtonRole.YesRole)
        # 在最后设置样式无法生效？！
        # self.msgbox.setStyleSheet(StyleSheetHelper.load_qss(name='msgbox'))


class QWarnMessageBox(QAbstractMessageBox):
    def __init__(self, parent: QWidget, text: str):
        super().__init__(parent, text, 'icon/msgbox_warning.png')
        self.btn_yes = self.msgbox.addButton(parent.tr('确认'), QMessageBox.ButtonRole.YesRole)
        self.btn_no = self.msgbox.addButton(parent.tr('取消'), QMessageBox.ButtonRole.NoRole)
        self.msgbox.setDefaultButton(self.btn_no)

    def show(self):
        self.msgbox.exec()
        if self.msgbox.clickedButton() == self.btn_yes:
            return QMSG_BOX_REPLY_YES
        return QMSG_BOX_REPLY_NO


class QuestionMessageBox(QAbstractMessageBox):
    def __init__(self, parent: QWidget, text: str):
        super().__init__(parent, text, 'icon/msgbox_question.png')
        # self.msgbox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        self.btn_yes = self.msgbox.addButton(parent.tr('确认'), QMessageBox.ButtonRole.YesRole)
        self.btn_no = self.msgbox.addButton(parent.tr('取消'), QMessageBox.ButtonRole.NoRole)
        self.msgbox.setDefaultButton(self.btn_no)
        # TODO 消息框不同按钮不同样式
        # https://stackoverflow.com/questions/66604761/is-there-a-way-to-change-the-stylesheet-of-just-ok-button-of-all-the-qmessagebox

    def show(self):
        self.msgbox.exec()
        if self.msgbox.clickedButton() == self.btn_yes:
            return QMSG_BOX_REPLY_YES
        return QMSG_BOX_REPLY_NO


# https://github.com/fbjorn/QtWaitingSpinner
class WaitingSpinner(QWidget):

    def __init__(self, parent, centerOnParent=True, disableParentWhenSpinning=False,
                 modality=Qt.WindowModality.NonModal, roundness=100., opacity=None, fade=80., lines=20,
                 line_length=10, line_width=2, radius=10, speed=math.pi / 2, color=(0, 0, 0)):
        super().__init__(parent)

        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning

        self._color = QColor(*color)
        self._roundness = roundness
        self._minimumTrailOpacity = math.pi
        self._trailFadePercentage = fade
        self._revolutionsPerSecond = speed
        self._numberOfLines = lines
        self._lineLength = line_length
        self._lineWidth = line_width
        self._innerRadius = radius
        self._currentCounter = 0
        self._isSpinning = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.rotate)
        self.updateSize()
        self.updateTimer()
        self.hide()

        self.setWindowModality(modality)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, QPaintEvent):
        self.updatePosition()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(self._numberOfLines):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength, self._innerRadius + self._lineLength)
            rotateAngle = float(360 * i) / float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(i, self._currentCounter, self._numberOfLines)
            color = self.currentLineColor(
                distance,
                self._numberOfLines,
                self._trailFadePercentage,
                self._minimumTrailOpacity,
                self._color
            )
            painter.setBrush(color)
            painter.drawRoundedRect(
                QRect(0, -self._lineWidth / 2, self._lineLength, self._lineWidth),
                self._roundness,
                self._roundness,
                Qt.SizeMode.RelativeSize
            )
            painter.restore()

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parentWidget and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def setNumberOfLines(self, lines):
        self._numberOfLines = lines
        self._currentCounter = 0
        self.updateTimer()

    def setLineLength(self, length):
        self._lineLength = length
        self.updateSize()

    def setLineWidth(self, width):
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self.updateSize()

    @property
    def color(self):
        return self._color

    @property
    def roundness(self):
        return self._roundness

    @property
    def minimumTrailOpacity(self):
        return self._minimumTrailOpacity

    @property
    def trailFadePercentage(self):
        return self._trailFadePercentage

    @property
    def revolutionsPersSecond(self):
        return self._revolutionsPerSecond

    @property
    def numberOfLines(self):
        return self._numberOfLines

    @property
    def lineLength(self):
        return self._lineLength

    @property
    def lineWidth(self):
        return self._lineWidth

    @property
    def innerRadius(self):
        return self._innerRadius

    @property
    def isSpinning(self):
        return self._isSpinning

    def setRoundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def setColor(self, color=Qt.GlobalColor.black):
        self._color = QColor(color)

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self._revolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self._trailFadePercentage = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self._minimumTrailOpacity = minimumTrailOpacity

    def rotate(self):
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0
        self.update()

    def updateSize(self):
        size = (self._innerRadius + self._lineLength) * 2
        self.setFixedSize(size, size)

    def updateTimer(self):
        self._timer.setInterval(1000 / (self._numberOfLines * self._revolutionsPerSecond))

    def updatePosition(self):
        if self.parentWidget() and self._centerOnParent:
            self.move(
                self.parentWidget().width() / 2 - self.width() / 2,
                self.parentWidget().height() / 2 - self.height() / 2
            )

    def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, colorinput):
        color = QColor(colorinput)
        if countDistance == 0:
            return color
        minAlphaF = minOpacity / 100.0
        distanceThreshold = int(math.ceil((totalNrOfLines - 1) * trailFadePerc / 100.0))
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float(distanceThreshold + 1)
            resultAlpha = color.alphaF() - gradient * countDistance
            # If alpha is out of bounds, clip it.
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)
        return color

