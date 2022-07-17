#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt6 import QtWidgets
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
        self.update_state()

    def set_connect(self):
        self.prePageBtn.clicked.connect(self.on_prev_page)
        self.nextPageBtn.clicked.connect(self.on_next_page)
        self.switchPageBtn.clicked.connect(self.go_switch_page)
        self.searchBtn.clicked.connect(self.go_search)

    def update_state(self):
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

    def closeEvent(self, event):
        self.close_db()


class ProgressDataWindow(DataGridWindow):
    def __init__(self):
        columns = dict(zip(
            ['id', 'origin', 'resp_code', 'create_time'],
            ['ID', 'URL/FILE路径', '状态码', '创建时间']
        ))
        super().__init__(table='crawlstat', columns=columns)


class ExtractDataWindow(DataGridWindow):
    def __init__(self):
        columns = dict(zip(
            ['id', 'origin', 'sensitive_type', 'count', 'create_time'],
            ['ID', '敏感内容来源', '敏感种类', '数量', '创建时间']
        ))
        super().__init__(table='extractor', columns=columns)


class WhiteListDataWindow(DataGridWindow):
    def __init__(self):
        columns = dict(zip(
            ['id', 'white_type', 'ioc', 'create_time'],
            ['ID', '种类', '内容', '创建时间']
        ))
        super().__init__(table='whitelist', columns=columns)
