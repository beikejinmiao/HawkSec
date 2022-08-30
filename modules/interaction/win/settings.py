#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QPalette, QColor, QCursor
from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QFileDialog
from modules.gui.ui_settings import Ui_Form
from modules.interaction.win.tableview import WhiteListDataWindow
from modules.interaction.win.msgbox import QInfoMessageBox, QWarnMessageBox
from libs.enums import TABLES
from libs.pyaml import configure
from libs.pysqlite import Sqlite
from libs.regex import is_valid_domain
from conf.paths import PRIVATE_RESOURCE_HOME, IMAGE_HOME
from utils.filedir import StyleSheetHelper
from utils.filedir import reader


class Setting(object):
    def __init__(self, timeout=5, builtin_alexa=True, white_domain=None, white_file=None):
        self.timeout = configure.get('timeout', timeout)
        self.builtin_alexa = configure.get('builtin_alexa', builtin_alexa)
        self.white_domain = set() if white_domain is None else set(white_domain)
        self.white_file = set() if white_file is None else set(white_file)


setting = Setting()


class SettingsWindow(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #
        self.setting = setting
        self.__init_ui()
        self.__init_state()
        #
        self.sqlite = Sqlite()
        self.whiteDomTableView = None     
        self.whiteFileTableView = None
        self._existed_domain = None
        self._existed_file = None
        self.cwd = os.getcwd()

    def __init_ui(self):
        QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)           # 隐藏边框
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 设置窗口背景透明
        self.closeBtnLabel.setText('')
        #
        win_sheet = StyleSheetHelper.load_qss(name='settings').replace('IMAGE_HOME', IMAGE_HOME)
        self.setStyleSheet(win_sheet)
        # 设置PlaceholderText样式(必须在setStyleSheet后设置)
        for text_edit in [self.whiteDomTextEdit, self.whiteFileTextEdit]:
            palette = text_edit.palette()
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 100))
            text_edit.setPalette(palette)
        #
        for button in [self.closeBtnLabel, self.importDomLabel, self.importFileLabel,
                       self.checkWhiteDomBtn, self.checkWhiteFileBtn, self.builtinAlexaEnableBox,
                       self.timeoutComboBox, self.saveBtn, self.cancelBtn]:
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # 窗体自定义阴影
        self.render_shadow()

    def __init_state(self):
        index = self.timeoutComboBox.findText(str(self.setting.timeout), Qt.MatchFlag.MatchFixedString)
        if index >= 0:
            self.timeoutComboBox.setCurrentIndex(index)
        #
        self.importDomLabel.clicked.connect(lambda: self.import_file(category='domain'))
        self.importFileLabel.clicked.connect(lambda: self.import_file(category='urlfile'))
        self.checkWhiteDomBtn.clicked.connect(self.show_white_dom_win)
        self.checkWhiteFileBtn.clicked.connect(self.show_white_file_win)
        self.saveBtn.clicked.connect(self.save)
        self.closeBtnLabel.clicked.connect(self.close)
        self.cancelBtn.clicked.connect(self.close)

    def render_shadow(self):
        """
        https://blog.csdn.net/mahuatengmmp/article/details/113772969
        """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)  # 偏移
        shadow.setBlurRadius(12)  # 阴影半径
        shadow.setColor(QColor(128, 128, 255))  # 阴影颜色
        self.centralWidget.setGraphicsEffect(shadow)  # 将设置套用到widget窗口中

    def import_file(self, category='domain'):
        filenames, filetypes = QFileDialog.getOpenFileNames(self, '打开文件',
                                                            self.cwd, 'Text Files (*.txt);;All Files (*)')
        for filename in filenames:
            print(filename)

        text_edit = self.whiteDomTextEdit
        if category == 'urlfile':
            text_edit = self.whiteFileTextEdit

        for filename in filenames:
            for line in reader(filename):
                text_edit.appendPlainText(line)

    def __check_inputs(self):
        self.setting.timeout = int(self.timeoutComboBox.currentText())
        #
        for text_edit, dataset in [(self.whiteDomTextEdit, self.setting.white_domain),
                                   (self.whiteFileTextEdit, self.setting.white_file)]:
            plain_text = text_edit.toPlainText()
            for line in plain_text.split('\n'):
                for item in line.split(','):
                    item = item.strip()
                    if len(item) > 0:
                        dataset.add(item)
        #
        if self.builtinAlexaEnableBox.isChecked():
            self.setting.builtin_alexa = True
        else:
            self.setting.builtin_alexa = False

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
        not_valid_domains = set()
        for item in self.setting.white_domain:
            if not is_valid_domain(item):
                not_valid_domains.add(item)
        if len(not_valid_domains) > 0:
            self.setting.white_domain = self.setting.white_domain - not_valid_domains
            # QInfoMessageBox('下列域名格式不合法将被忽略:\n%s' % ','.join(not_valid_domains)).exec()
        #
        try:
            configure['timeout'] = self.setting.timeout
            configure['builtin_alexa'] = self.setting.builtin_alexa
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
            if len(white_insert) > 0:
                self.sqlite.insert_many(TABLES.WhiteList.value, white_insert)
            QInfoMessageBox("保存成功").exec()
            self.close()
        except Exception as e:
            QWarnMessageBox("保存失败，错误原因：" + str(e)).exec()

    def show_white_dom_win(self):
        self.whiteDomTableView = WhiteListDataWindow(white_type='domain')        # 窗口关闭后销毁对象
        self.whiteDomTableView.show()

    def show_white_file_win(self):
        self.whiteFileTableView = WhiteListDataWindow(white_type='file')        # 窗口关闭后销毁对象
        self.whiteFileTableView.show()

    def closeEvent(self, event):
        self.sqlite.close()

