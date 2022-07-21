#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread
from modules.ui.ui_main_window import Ui_MainWindow as UiMainWindow
from modules.action.manager import TaskManager
from modules.action.win.sshconfig import SshConfigWindow
from modules.action.win.settings import SettingWindow
from modules.action.win.tableview import ProgressDataWindow, ExtractDataWindow
from libs.logger import QLogTailReader

MONIT_TARGET = ''


class MainWindow(UiMainWindow, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settingWindow = SettingWindow()
        self.sshConfigWindow = SshConfigWindow()
        self.progressWindow = None  # ProgressDataWindow()
        self.extractWindow = None   # ExtractDataWindow()
        #
        self.__init_state()
        #
        self.target = ''
        self.protocol = 'https'
        self.types = list()
        self.task_manager = None
        self.log_viewer = None

    def __init_state(self):
        self.httpsRadioBtn.setChecked(True)
        self.extUrlCheckBox.setChecked(True)
        self.stopBtn.setEnabled(False)
        #
        self.menuActionGeneral.triggered.connect(self.settingWindow.show)
        self.sftpRadioBtn.clicked.connect(self.show_sshconf_win)
        self.startBtn.clicked.connect(self.start)
        self.stopBtn.clicked.connect(self.stop)
        self.exitBtn.clicked.connect(self.close)
        self.checkProgressBtn.clicked.connect(self.show_progress_win)
        self.checkExtractBtn.clicked.connect(self.show_extract_win)
        #

    def __toggle_state(self, enable=True):
        """
        开始/停止时,切换按钮和输入框状态
        """
        self.startBtn.setEnabled(enable)
        self.stopBtn.setEnabled(not enable)
        self.targetLineEdit.setEnabled(enable)
        for ix in range(self.protocolVLayout.count()):
            child = self.protocolVLayout.itemAt(ix).widget()
            child.setEnabled(enable)
        for ix in range(self.mtypeGridLayout.count()):
            child = self.mtypeGridLayout.itemAt(ix).widget()
            child.setEnabled(enable)

    def __log_append2gui(self, text):
        self.logTextBox.appendPlainText(text)

    def __start_log_reader(self):
        self.log_viewer = QThread()
        self.log_reader = QLogTailReader()
        self.log_reader.moveToThread(self.log_viewer)
        # Connect signals and slots
        self.log_viewer.started.connect(self.log_reader.run)
        self.log_reader.finished.connect(self.log_viewer.quit)
        self.log_reader.finished.connect(self.log_reader.deleteLater)
        self.log_viewer.finished.connect(self.log_viewer.deleteLater)
        self.log_reader.progress.connect(self.__log_append2gui)
        # Start the thread
        self.log_viewer.start()

        # Final resets
        self.log_viewer.finished.connect(
            lambda: self.startBtn.setEnabled(True)
        )

    def _check_inputs(self):
        self.target = self.targetLineEdit.text().strip()
        if len(self.target) <= 0:
            QtWidgets.QMessageBox.warning(self, "提醒", "监控对象为空！请输入监控对象：IP/域名/URL")
            return False
        # 访问协议
        for ix in range(self.protocolVLayout.count()):
            child = self.protocolVLayout.itemAt(ix).widget()
            if isinstance(child, QtWidgets.QRadioButton) and child.isChecked():
                self.protocol = child.text().lower()
        # 监控内容/敏感类型
        self.types = list()
        for ix in range(self.mtypeGridLayout.count()):
            child = self.mtypeGridLayout.itemAt(ix).widget()
            if isinstance(child, QtWidgets.QCheckBox) and child.isChecked():
                self.types.append(ix)
        if len(self.types) <= 0:
            QtWidgets.QMessageBox.warning(self, "提醒", "未选择监控内容！")
            return False
        return True

    def show_sshconf_win(self):
        self.sshConfigWindow.hostLineEdit.setText(self.targetLineEdit.text().strip())
        self.sshConfigWindow.show()

    def show_progress_win(self):
        self.progressWindow = ProgressDataWindow()      # 窗口关闭后销毁对象
        self.progressWindow.show()

    def show_extract_win(self):
        self.extractWindow = ExtractDataWindow()        # 窗口关闭后销毁对象
        self.extractWindow.show()

    def start(self):
        if not self._check_inputs():
            return
        auth_config = None
        if self.protocol == 'sftp':
            auth_config = self.sshConfigWindow.config
        self.task_manager = TaskManager(self.target,
                                        flags=self.types,
                                        protocol=self.protocol,
                                        auth_config=auth_config)
        if self.log_viewer is None:
            self.__start_log_reader()
        self.__toggle_state(enable=False)
        self.task_manager.start()

    def stop(self):
        self.task_manager.stop()
        self.__toggle_state(enable=True)
        del self.task_manager

