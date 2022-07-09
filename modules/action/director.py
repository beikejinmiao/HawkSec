#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
from collections import namedtuple
from PyQt6 import QtWidgets, QtCore, Qt
from modules.ui.ui_main_window import Ui_MainWindow as UiMainWindow
from modules.ui.ui_help_settings import Ui_Form as UiSettingForm
from modules.ui.ui_ssh_config import Ui_Dialog as UiSshConfigDialog
from modules.action.manager import TaskManager
from utils.mixed import ssh_accessible
from libs.pyaml import configure
from libs.logger import logger


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
        self.protocol = 'http'
        self.types = list()
        self.task_manager = None

    def __init_state(self):
        self.httpRadioBtn.setChecked(True)
        self.extUrlCheckBox.setChecked(True)
        #
        self.sftpRadioBtn.clicked.connect(self.show_sshconf_win)
        self.startBtn.clicked.connect(self.start)
        self.stopBtn.clicked.connect(self.stop)
        self.exitBtn.clicked.connect(self.close)

    def _check_inputs(self):
        self.target = self.monitTarget.text().strip()
        if len(self.target) <= 0:
            QtWidgets.QMessageBox.warning(self, "提醒", "监控对象为空！请输入监控对象：IP/域名/URL")
            return False
        # for radioBtn in self.protocolVLayout.children():
        for radioBtn in [self.httpRadioBtn, self.httpsRadioBtn, self.sftpRadioBtn]:
            if radioBtn.isChecked():
                self.protocol = radioBtn.text().lower()
        self.types = list()
        # for i, checkBox in enumerate(self.mtypeGridLayout.children()):
        for i, checkBox in enumerate([self.extUrlCheckBox, self.idcardCheckBox, self.keywordCheckBox]):
            if checkBox.isChecked():
                self.types.append(i)
        if len(self.types) <= 0:
            QtWidgets.QMessageBox.warning(self, "提醒", "未选择监控内容！")
            return False
        return True

    def show_sshconf_win(self):
        self.sshConfigWindow.hostLineEdit.setText(self.monitTarget.text().strip())
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
        thread.start()
        # self.task_manager.start()     # 阻塞GUI主进程

    def stop(self):
        if self.task_manager is not None:
            self.task_manager.stop()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
    window.show()
    sys.exit(app.exec())



