#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import math
from PyQt6 import QtWidgets
from libs.enums import TABLES
from libs.pysqlite import Sqlite
from conf.paths import DUMP_HOME
from modules.ui.ui_tableview import Ui_Form
from modules.action.dbmodel import TablePageModel


class DataGridWindow(TablePageModel, Ui_Form, QtWidgets.QWidget):
    def __init__(self, table, columns):
        TablePageModel.__init__(self, table, columns)
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        # super().__init__(table, columns)
        self.setupUi(self)
        self.tableView.setModel(self.query_model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.set_connect()
        self.update_ui_state()
        #
        self.sqlite = Sqlite()

    def set_connect(self):
        self.prePageBtn.clicked.connect(self.on_prev_page)
        self.nextPageBtn.clicked.connect(self.on_next_page)
        self.switchPageBtn.clicked.connect(self.go_switch_page)
        self.searchBtn.clicked.connect(self.go_search)
        self.refreshBtn.clicked.connect(self.refresh)
        self.dumpBtn.clicked.connect(self.dump)

    def update_ui_state(self):
        self.curPageLineEdit.setText(str(self.cur_page))
        self.totalPageLineEdit.setText(str(self.total_page))
        if self.cur_page <= 1:
            self.prePageBtn.setEnabled(False)
        else:
            self.prePageBtn.setEnabled(True)

        if self.cur_page >= self.total_page:
            self.nextPageBtn.setEnabled(False)
        else:
            self.nextPageBtn.setEnabled(True)

    def go_switch_page(self):
        page = self.switchPageLineEdit.text().strip()
        if page == "":
            QtWidgets.QMessageBox.information(self, "提示", "请输入跳转页面")
            return
        if not page.isdigit():
            QtWidgets.QMessageBox.information(self, "提示", "请输入数字")
            return
        page_idx = int(page)
        if page_idx > self.total_page or page_idx < 1:
            QtWidgets.QMessageBox.information(self, "提示", "没有指定的页，清重新输入")
            return
        self.switch_page = page_idx
        self.on_switch_page()

    def go_search(self):
        origin = self.originLineEidt.text().strip()
        if origin == "":
            QtWidgets.QMessageBox.information(self, "提示", "请输入查询内容")
            return
        code = self.codeComboBox.currentIndex()

    def refresh(self):
        self.cur_page = 1
        self.query_page(page=1)
        self.update_total_count()

    def dump(self):
        filepath, ok = QtWidgets.QFileDialog.getSaveFileName(self, "保存文件",
                                                             os.path.join(DUMP_HOME, "%s.csv" % self.table))
        if ok:
            try:
                self.sqlite.dump(self.table, filepath)
                QtWidgets.QMessageBox.information(self, "提示", "保存成功. 文件路径: " + filepath)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "提示", "保存失败. 错误原因: " + str(e))

    def closeEvent(self, event):
        self.close_db()


class ProgressDataWindow(DataGridWindow):
    def __init__(self):
        columns = dict(zip(
            ['id', 'origin', 'resp_code', 'desc', 'create_time'],
            ['ID', 'URL/FILE路径', '状态码', '描述', '创建时间']
        ))
        super().__init__(table=TABLES.CrawlStat.value, columns=columns)


class ExtractDataWindow(DataGridWindow):
    def __init__(self):
        columns = dict(zip(
            ['id', 'origin', 'sensitive_name', 'result', 'count', 'create_time'],
            ['ID', 'URL/FILE路径', '敏感类型', '内容', '数量', '创建时间']
        ))
        super().__init__(table=TABLES.Extractor.value, columns=columns)


class WhiteListDataWindow(DataGridWindow):
    def __init__(self):
        columns = dict(zip(
            ['id', 'white_type', 'ioc', 'create_time'],
            ['ID', '种类', '内容', '创建时间']
        ))
        super().__init__(table=TABLES.WhiteList.value, columns=columns)
