#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QThread
from conf.paths import LOG_FILEPATH
from libs.enums import SENSITIVE_FLAG
from modules.ui.ui_main_window import Ui_MainWindow as UiMainWindow
from modules.action.manager import TaskManager
from modules.action.win.sshconfig import SshConfigWindow
from modules.action.win.settings import SettingWindow
from modules.action.win.tableview import ProgressDataWindow, ExtractDataWindow, SensitiveDataWindow
from modules.action.metric import QCrawlExtProgress
from libs.logger import QLogTailReader

MONIT_TARGET = ''


class MainWindow(UiMainWindow, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settingWindow = None
        self.sshConfigWindow = SshConfigWindow()
        self.progressWindow = None  # ProgressDataWindow()
        self.extractWindow = None   # ExtractDataWindow()
        self.sensitiveWindow = None  # SensitiveDataWindow()
        #
        self.__init_ui_state()
        #
        self.target = ''
        self.protocol = 'https'
        self.sensitive_flags = list()
        self._keywords = None
        self.task_manager = None
        self.metric_thread = None
        self.log_viewer = None

    def __init_ui_state(self):
        self.httpsRadioBtn.setChecked(True)
        self.extUrlCheckBox.setChecked(True)
        self.stopBtn.setEnabled(False)
        #
        self.menuActionGeneral.triggered.connect(self.show_setting_win)
        self.sftpRadioBtn.clicked.connect(self.show_sshconf_win)
        self.startBtn.clicked.connect(self.start)
        self.stopBtn.clicked.connect(lambda: self.terminate(notice=True))
        self.exitBtn.clicked.connect(self.close)
        self.checkProgressBtn.clicked.connect(self.show_progress_win)
        self.checkExtractBtn.clicked.connect(self.show_extract_win)
        self.checkSensitiveBtn.clicked.connect(self.show_sensitive_win)
        self.update_ui_metric(QCrawlExtProgress.metric())
        # 设置PlaceholderText字体颜色和透明度
        palette = self.keywordLineEdit.palette()
        palette.setColor(QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(0, 0, 0, 100))
        self.keywordLineEdit.setPalette(palette)
        # self.__pre_load_log()

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
        for ix in range(self.sflagGridLayout.count()):
            child = self.sflagGridLayout.itemAt(ix).widget()
            child.setEnabled(enable)

    def __log2gui(self, text):
        self.logTextBox.appendPlainText(text)

    def __pre_load_log(self):
        with open(LOG_FILEPATH, 'rb') as fopen:
            # seek the end of the file
            fopen.seek(0, os.SEEK_END)
            # 逆序读取最多1500个字符
            fopen.seek(max(-fopen.tell(), -1500), os.SEEK_END)
            lines = fopen.readlines()
            if len(lines) <= 1:
                return
            for i in range(1, len(lines)):
                self.__log2gui(str(lines[i], encoding='utf-8').strip())

    def __start_log_reader(self):
        self.log_viewer = QThread()
        self.log_reader = QLogTailReader()
        self.log_reader.moveToThread(self.log_viewer)
        # Connect signals and slots
        self.log_viewer.started.connect(self.log_reader.run)
        self.log_reader.finished.connect(self.log_viewer.quit)
        self.log_reader.finished.connect(self.log_reader.deleteLater)
        self.log_viewer.finished.connect(self.log_viewer.deleteLater)
        self.log_reader.readline.connect(self.__log2gui)
        # Start the thread
        self.log_viewer.start()

        # Final resets
        self.log_viewer.finished.connect(
            lambda: self.startBtn.setEnabled(True)
        )

    def _check_inputs(self):
        self.target = self.targetLineEdit.text().strip()
        if len(self.target) <= 0:
            QMessageBox.warning(self, "提醒", "监控对象为空！请输入监控对象：IP/域名/URL")
            return False
        # 访问协议
        for ix in range(self.protocolVLayout.count()):
            child = self.protocolVLayout.itemAt(ix).widget()
            if isinstance(child, QtWidgets.QRadioButton) and child.isChecked():
                self.protocol = child.text().lower()
        # 监控内容/敏感类型
        self.sensitive_flags = list()
        for ix in range(self.sflagGridLayout.count()):
            child = self.sflagGridLayout.itemAt(ix).widget()
            if isinstance(child, QtWidgets.QCheckBox) and child.isChecked():
                self.sensitive_flags.append(ix)
        if SENSITIVE_FLAG.KEYWORD in self.sensitive_flags:
            self._keywords = [item.strip() for item in self.keywordLineEdit.text().split(',')]
        if len(self.sensitive_flags) <= 0:
            QMessageBox.warning(self, "提醒", "未选择监控内容！")
            return False
        return True

    def show_setting_win(self):
        self.settingWindow = SettingWindow()
        self.settingWindow.show()

    def show_sshconf_win(self):
        self.sshConfigWindow.hostLineEdit.setText(self.targetLineEdit.text().strip())
        self.sshConfigWindow.show()

    def show_progress_win(self):
        self.progressWindow = ProgressDataWindow()      # 窗口关闭后销毁对象
        self.progressWindow.show()

    def show_extract_win(self):
        self.extractWindow = ExtractDataWindow()        # 窗口关闭后销毁对象
        self.extractWindow.show()

    def show_sensitive_win(self):
        self.sensitiveWindow = SensitiveDataWindow()        # 窗口关闭后销毁对象
        self.sensitiveWindow.show()

    def update_ui_metric(self, stat):
        if stat is None:
            return
        self.crawledCntLabel.setText(str(stat.get('crawl_total', 0)))
        self.faieldCntLabel.setText(str(stat.get('crawl_failed', 0)))
        self.hitCntLabel.setText(str(stat.get('origin_hit', 0)))
        # self.extUrlCntLabel.setText('%s个/%s次' % (stat.get('external_url_count', 0), stat.get('external_url_find', 0)))
        self.extUrlCntLabel.setText('%s个' % stat.get('external_url_count', 0))
        self.idcardCntLabel.setText('%s个/%s次' % (stat.get('idcard_count', 0), stat.get('idcard_find', 0)))
        self.keywordCntLabel.setText('%s个/%s次' % (stat.get('keyword_count', 0), stat.get('keyword_find', 0)))

    def start(self):
        if self.log_viewer is None:
            self.__start_log_reader()
        if not self._check_inputs():
            return
        reply = QMessageBox.information(self, "提醒", "重新开始将清除历史数据",
                                        buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Close,
                                        defaultButton=QMessageBox.StandardButton.Ok)
        if reply == QMessageBox.StandardButton.Close:
            return
        TaskManager.clear()
        self.update_ui_metric(dict())
        #
        auth_config = None
        if self.protocol == 'sftp':
            auth_config = self.sshConfigWindow.config
        self.task_manager = TaskManager(self.target,
                                        flags=self.sensitive_flags,
                                        protocol=self.protocol,
                                        keywords=self._keywords,
                                        auth_config=auth_config)
        self.metric_thread = QCrawlExtProgress()
        self.__toggle_state(enable=False)

        self.task_manager.start()
        self.metric_thread.start()
        self.task_manager.extractor.finished.connect(self.terminate)
        self.metric_thread.progress.connect(self.update_ui_metric)

    def terminate(self, notice=False):
        if notice:
            reply = QMessageBox.information(self, "提醒", "请确认是否终止目前任务，任务终止后需重新开始。",
                                            buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
                                            defaultButton=QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Cancel:
                return
        self.metric_thread.terminate()
        self.task_manager.terminate()
        self.__toggle_state(enable=True)
        del self.metric_thread
        del self.task_manager

    def closeEvent(self, event):
        reply = QMessageBox.warning(self, "提醒", "确认退出",
                                    buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
                                    defaultButton=QMessageBox.StandardButton.Cancel)
        if reply == QMessageBox.StandardButton.Ok:
            event.accept()
            if self.settingWindow:
                self.settingWindow.close()
            if self.sshConfigWindow:
                self.sshConfigWindow.close()
            if self.progressWindow:
                self.progressWindow.close()
            if self.extractWindow:
                self.extractWindow.close()
        else:
            event.ignore()

