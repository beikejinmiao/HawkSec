#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox, QSizePolicy, QLayout
from PyQt6.QtCore import QThread
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QColor
from modules.gui.ui_main_window import Ui_MainWindow as UiMainWindow
from modules.interaction.win.tableview import ExtractDataWindow
from modules.interaction.win.settings import SettingsWindow
from modules.interaction.win.help import HelpAboutWindow
from conf.paths import PRIVATE_RESOURCE_HOME, IMAGE_HOME
from pathlib import Path
from utils.filedir import StyleSheetHelper


class MainWindow(UiMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.extractWindow = None
        self.settingsWindow = None
        self.helpAboutWindow = None
        #
        self.__init_gui()
        self.__init_state()

    def __init_gui(self):
        QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(1)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabBarAutoHide(True)
        # StyleSheet中文件路径必须使用posix格式
        # https://stackoverflow.com/questions/51750501/do-not-insert-a-background-picture-into-widget-setstylesheet
        bg_pic_path = Path(os.path.join(IMAGE_HOME, 'bg.png')).as_posix()
        self.centralwidget.setStyleSheet('#centralwidget {border-image: url(%s);}' % bg_pic_path)
        # 使用border-image而不是background-image会让图片自适应widget大小
        # self.centralwidget.setStyleSheet(
        #     '#centralwidget {background-image: url(%s); background-repeat: no-repeat}' % bg_pic_path)
        label_images = zip([self.logoLabel, self.helpLabel, self.settingLabel,
                            self.robotLabel, self.robotLabel2, self.waitforGifLabel, self.finishIconLabel,
                            self.extUrlIconLabel, self.idcardIconLabel, self.keywordIconLabel,
                            self.minimizeBtnLabel, self.maximizeBtnLabel, self.closeBtnLabel],
                           ['logo.png', 'icon/help.png', 'icon/setting.png',
                            'robot.png', 'robot.png', 'icon/waitfor.png', 'icon/finish.png',
                            'icon/exturl.png', 'icon/idcard.png', 'icon/keyword.png',
                            'icon/minimize.png', 'icon/maximize.png', 'icon/close.png'])
        for label, img in label_images:
            label.setPixmap(QPixmap('image:%s' % img))
            # https://stackoverflow.com/questions/5653114/display-image-in-qt-to-fit-label-size
            label.setScaledContents(True)
            label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        # 设置整体样式
        win_sheet = StyleSheetHelper.load_qss(name='mainwin').replace('IMAGE_HOME', IMAGE_HOME)
        self.setStyleSheet(win_sheet)
        # 设置PlaceholderText字体颜色和透明度
        self.line_edits = (self.addressLineEdit, self.portLineEdit,
                           self.userLineEdit, self.passwdLineEdit, self.pathLineEdit)
        for line_edit in self.line_edits:
            palette = line_edit.palette()
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 100))
            line_edit.setPalette(palette)

    def __init_state(self):
        # 保证Layout隐藏部分组件时,剩余组件能自动移动填充(例如grid layout隐藏前两行,后几行能自动上移)
        # https://stackoverflow.com/questions/2293708/pyqt4-hide-widget-and-resize-window
        self.dynGridLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        #
        self.minimizeBtnLabel.clicked.connect(self.showMinimized)
        self.closeBtnLabel.clicked.connect(self.showMaximized)
        self.closeBtnLabel.clicked.connect(self.close)
        #
        self.__toggle_sftp()
        self.httpRadioBtn.clicked.connect(lambda: self.__toggle_sftp(visible=False))
        self.httpsRadioBtn.clicked.connect(lambda: self.__toggle_sftp(visible=False))
        self.sftpRadioBtn.clicked.connect(lambda: self.__toggle_sftp(visible=True))
        self.startBtn.clicked.connect(self.start)
        self.cancelBtn.clicked.connect(self.cancel)
        self.stopBtn.clicked.connect(self.terminate)
        self.returnBtn.clicked.connect(self.cancel)
        self.detailBtn.clicked.connect(self.show_extract_win)
        self.settingLabel.clicked.connect(self.show_settings_win)
        self.helpLabel.clicked.connect(self.show_help_win)

    def __toggle_sftp(self, visible=False):
        sftp_edits = (self.portLineEdit, self.userLineEdit, self.passwdLineEdit, self.pathLineEdit)
        for line_edit in sftp_edits:
            line_edit.setVisible(visible)

    def start(self):
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.monitTab, '')

    def cancel(self):
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.mainTab, '')

    def terminate(self):
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.finishTab, '')

    def show_extract_win(self):
        self.extractWindow = ExtractDataWindow()        # 窗口关闭后销毁对象
        self.extractWindow.show()

    def show_settings_win(self):
        self.settingsWindow = SettingsWindow()        # 窗口关闭后销毁对象
        self.settingsWindow.show()

    def show_help_win(self):
        self.helpAboutWindow = HelpAboutWindow()
        self.helpAboutWindow.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
