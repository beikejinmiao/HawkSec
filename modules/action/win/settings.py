#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from collections import namedtuple
from PyQt6 import QtWidgets
from modules.ui.ui_help_settings import Ui_Form
from libs.enums import TABLES
from libs.pyaml import configure
from libs.pysqlite import Sqlite
from libs.regex import is_valid_domain
from modules.action.win.tableview import WhiteListDataWindow


class Setting(object):
    def __init__(self, timeout=5, enable_builtin_domain=0, white_domain=None, white_file=None):
        self.timeout = timeout
        self.enable_builtin_domain = enable_builtin_domain
        self.white_domain = set() if white_domain is None else set(white_domain)
        self.white_file = set() if white_file is None else set(white_file)


class SettingWindow(Ui_Form, QtWidgets.QWidget):

    Config = namedtuple('Config', ['timeout', 'enable_builtin_domain', 'white_domain', 'white_file'])

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__init_state()
        self.sqlite = Sqlite()
        self.setting = Setting()
        self.whiteDomWindow = None
        self.whiteFileWindow = None

        self._existed_domain = None
        self._existed_file = None

    def __init_state(self):
        self.timeoutLineEdit.setText(str(configure.get('timeout', 5)))
        # self.whiteDomTextEdit.setPlainText('')
        # self.whiteFileTextEdit.setPlainText('')
        self.saveBtn.clicked.connect(self.save)
        self.exitBtn.clicked.connect(self.close)
        self.checkWhiteDomBtn.clicked.connect(self.show_white_dom_win)
        self.checkWhiteFileBtn.clicked.connect(self.show_white_file_win)

    def __check_timeout(self):
        timeout = self.timeoutLineEdit.text().strip()
        if len(timeout) <= 0:
            QtWidgets.QMessageBox.warning(self, "提醒", '超时时间内容为空！')
            return False
        if not re.match(r'^\d+(\.\d+)?$', timeout) or float(timeout) <= 0.0:
            QtWidgets.QMessageBox.warning(self, "提醒", '超时时间格式错误！请输入大于零的数字')
            return False
        #
        self.setting.timeout = float(timeout)
        return True

    def __check_inputs(self):
        if not self.__check_timeout():
            return
        #
        plain_text = self.whiteDomTextEdit.toPlainText()
        for line in plain_text.split('\n'):
            for item in line.split(','):
                item = item.strip()
                if is_valid_domain(item) > 0:
                    self.setting.white_domain.add(item)
        plain_text = self.whiteFileTextEdit.toPlainText()
        for line in plain_text.split('\n'):
            for item in line.split(','):
                item = item.strip()
                if len(item) > 0:
                    self.setting.white_file.add(item)

    def __load_existed(self):
        if self._existed_domain is None:
            self._existed_domain = set()
            records = self.sqlite.select('SELECT ioc FROM %s WHERE white_type="domain"' % TABLES.WhiteList.value)
            for record in records:
                self._existed_domain.add(record[0])
        #
        if self._existed_file is None:
            self._existed_file = set()
            records = self.sqlite.select('SELECT ioc FROM %s WHERE white_type="file"' % TABLES.WhiteList.value)
            for record in records:
                self._existed_file.add(record[0])

    def save(self):
        self.__check_inputs()
        #
        try:
            configure['timeout'] = self.setting.timeout
            configure.save()
            #
            self.__load_existed()
            white_insert = list()
            if len(self.setting.white_domain) > 0:
                new_white_domain = self.setting.white_domain - self._existed_domain
                if len(new_white_domain) > 0:
                    # 将新添加的白名单保存至已存在名单,避免多次查询数据库
                    self._existed_domain = self._existed_domain | new_white_domain
                    white_insert.extend([
                        {'white_type': 'domain', 'ioc': domain, 'desc': '自定义'} for domain in new_white_domain
                    ])
            if len(self.setting.white_file) > 0:
                new_white_file = self.setting.white_file - self._existed_file
                if len(new_white_file) > 0:
                    self._existed_file = self._existed_file | new_white_file
                    white_insert.extend([
                        {'white_type': 'file', 'ioc': file, 'desc': '自定义'} for file in new_white_file
                    ])
            self.sqlite.insert_many(TABLES.WhiteList.value, white_insert)
            QtWidgets.QMessageBox.information(self, "提醒", "保存成功,请点击查看具体内容")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "提醒", "保存失败，错误原因：" + str(e))

    def show_white_dom_win(self):
        self.whiteDomWindow = WhiteListDataWindow(white_type='domain')        # 窗口关闭后销毁对象
        self.whiteDomWindow.show()

    def show_white_file_win(self):
        self.whiteFileWindow = WhiteListDataWindow(white_type='file')        # 窗口关闭后销毁对象
        self.whiteFileWindow.show()

    def closeEvent(self, event):
        self.sqlite.close()

