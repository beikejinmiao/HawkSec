#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import namedtuple
from PyQt6 import QtWidgets
from modules.ui.ui_ssh_config import Ui_Dialog
from utils.mixed import ssh_accessible
from libs.pyaml import configure


class SshConfigWindow(Ui_Dialog, QtWidgets.QWidget):
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
