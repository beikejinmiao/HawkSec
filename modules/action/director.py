#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
from collections import namedtuple
from PyQt6 import QtWidgets, QtCore, Qt
from PyQt6.QtCore import QThread, pyqtSignal
from modules.ui.ui_main_window import Ui_MainWindow as UiMainWindow
from modules.ui.ui_help_settings import Ui_Form as UiSettingForm
from modules.ui.ui_ssh_config import Ui_Dialog as UiSshConfigDialog
from modules.action.manager import TaskManager
from utils.mixed import ssh_accessible
from libs.pyaml import configure
from libs.logger import QLogTailReader


MONIT_TARGET = ''


class SettingWindow(UiSettingForm, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class SshConfigWindow(UiSshConfigDialog, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 在SSH配置页面未关闭的情况下，禁止操作主页面
        # https://stackoverflow.com/questions/50631443/how-to-make-application-window-stay-on-top-in-pyqt5
        # https://stackoverflow.com/questions/18256459/qdialog-prevent-closing-in-python-and-pyqt
        # self.setWindowFlags(QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.CustomizeWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        #
        self.__init_state()
        self.accessible = False
        self.config = dict()

    def __init_state(self):
        self.testBtn.clicked.connect(self.check_accessible)
        self.doneBtn.clicked.connect(self.save_config)
        self.elements = ('host', '地址', self.hostLineEdit), ('port', '端口', self.portLineEdit), \
                        ('username', '用户名', self.userLineEdit), ('password', '密码', self.passwdLineEdit), \
                        ('path', '路径', self.pathLineEdit)
        for field, name, ele in self.elements:
            value = configure['ssh'][field]
            if field not in ('host', 'password') and value:
                ele.setText(str(value))

    SSH_CONFIG = namedtuple('SSH_CONFIG', ['host', 'port', 'username', 'password', 'path'])

    def get_config(self):
        return self.SSH_CONFIG(
            host=self.hostLineEdit.text().strip(),
            port=int(self.portLineEdit.text().strip()),
            username=self.userLineEdit.text().strip(),
            password=self.passwdLineEdit.text().strip(),
            path=self.pathLineEdit.text().strip()
        )

    def check_input_correct(self):
        empty = []
        for field, name, ele in self.elements:
            if len(ele.text().strip()) <= 0:
                empty.append(name)
        if len(empty) > 0:
            QtWidgets.QMessageBox.warning(self, "提醒", '/'.join(empty) + '内容为空！')
            return False
        if not self.portLineEdit.text().strip().isdigit():
            QtWidgets.QMessageBox.warning(self, "提醒", '端口格式错误！')
            return False
        return True

    def check_accessible(self):
        if not self.check_input_correct():
            self.accessible = False
            return None
        #
        config = self.get_config()
        try:
            ssh_accessible(config.host, port=config.port, username=config.username, password=config.password)
        except Exception as e:
            self.accessible = False
            QtWidgets.QMessageBox.warning(self, "提醒", '访问SSH服务器错误！原因: ' + str(e))
            return None
        QtWidgets.QMessageBox.information(self, "信息", '访问ssh://{username}@{host}:{port}成功'.format(
                                        username=config.username, host=config.host, port=config.port))
        self.accessible = True      # 在已校验访问成功后,保存配置时无需再次校验
        self.config = config._asdict()
        return config

    def save_config(self):
        if not self.accessible:
            config = self.check_accessible()
            if not config:
                return
        else:
            config = self.get_config()
        self.config = config._asdict()
        for field in self.config.keys():
            configure['ssh'][field] = self.config[field]
        configure.save()
        self.accessible = False     # 设置为False,重新打开页面时需再次访问校验
        self.close()


class MainWindow(UiMainWindow, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settingWindow = SettingWindow()
        self.sshConfigWindow = SshConfigWindow()
        self.menuActionGeneral.triggered.connect(self.settingWindow.show)
        #
        self.__init_state()
        #
        self.target = ''
        self.protocol = 'https'
        self.types = list()
        self.task_manager = None

    def __init_state(self):
        self.httpsRadioBtn.setChecked(True)
        self.extUrlCheckBox.setChecked(True)
        self.stopBtn.setEnabled(False)
        #
        self.sftpRadioBtn.clicked.connect(self.show_sshconf_win)
        self.startBtn.clicked.connect(self.start)
        self.stopBtn.clicked.connect(self.stop)
        self.exitBtn.clicked.connect(self.close)
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
        thread = threading.Thread(target=self.task_manager.start)
        self.__start_log_reader()
        self.__toggle_state(enable=False)
        thread.start()
        #

    def stop(self):
        self.__toggle_state(enable=True)
        if self.task_manager is not None:
            self.task_manager.stop()


