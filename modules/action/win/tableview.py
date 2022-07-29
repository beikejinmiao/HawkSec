#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QHeaderView
from libs.enums import TABLES, SENSITIVE_NAME, tables_cn_name
from libs.pysqlite import Sqlite
from conf.paths import DUMP_HOME
from modules.ui.ui_tableview import Ui_Form
from modules.action.dbmodel import TablePageModel


class DataGridWindow(TablePageModel, Ui_Form, QtWidgets.QWidget):
    def __init__(self, table, columns, init_where=None, column_modes=None):
        TablePageModel.__init__(self, table, columns, init_where=init_where)
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        # super().__init__(table, columns)
        self.setupUi(self)
        self.custom_ui()
        self.tableView.setModel(self.query_model)
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header = self.tableView.horizontalHeader()
        for i, mode in enumerate(column_modes):
            header.setSectionResizeMode(i, mode)
        # self.tableView.showRow(0)

        self.set_connect()
        self.update_ui_state()

    def custom_ui(self):
        pass

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
        self.totalRecordlineEdit.setText(str(self.total_record))
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
        # origin = self.originLineEidt.text().strip()
        # if origin == "":
        #     QtWidgets.QMessageBox.information(self, "提示", "请输入查询内容")
        #     return
        code = self.searchCodeComboBox.currentText()
        if code.upper() == 'ALL':
            self.db_where = None
        else:
            if self.table == TABLES.CrawlStat.value:
                self.db_where = 'resp_code=%s' % code
            elif self.table == TABLES.Extractor.value or self.table == TABLES.Sensitives.value:
                self.db_where = 'sensitive_name="%s"' % code

        self.update_total_count()
        self.cur_page = 1
        self.query_page(page=1)

    def refresh(self):
        self.cur_page = 1
        self.query_page(page=1)
        self.update_total_count()

    def dump(self):
        filepath, ok = QtWidgets.QFileDialog.getSaveFileName(
            self, "保存文件", os.path.join(DUMP_HOME, "%s.csv" % tables_cn_name.get(self.table, self.table))
        )
        if ok:
            try:
                self.sqlite.dump(self.table, filepath, columns=self.columns)
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
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents,
                        QHeaderView.ResizeMode.ResizeToContents]
        super().__init__(table=TABLES.CrawlStat.value, columns=columns, column_modes=column_modes)

    def custom_ui(self):
        self.searchCodeLabel.setText('状态码')
        codes = self.sqlite.select('SELECT DISTINCT resp_code FROM %s ORDER BY resp_code' % self.table)
        codes = [item[0] for item in codes]
        for i, code in enumerate(codes):
            self.searchCodeComboBox.insertItem(i+1, str(code))


class ExtractDataWindow(DataGridWindow):
    def __init__(self):
        columns = dict(zip(
            ['id', 'origin', 'sensitive_name', 'content', 'count', 'create_time'],
            ['ID', 'URL/FILE路径', '敏感类型', '敏感内容', '数量', '创建时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents]
        super().__init__(table=TABLES.Extractor.value, columns=columns, column_modes=column_modes)

    def custom_ui(self):
        self.searchCodeLabel.setText('敏感类型')
        names = [SENSITIVE_NAME.URL.value, SENSITIVE_NAME.IDCARD.value, SENSITIVE_NAME.KEYWORD.value]
        for i, name in enumerate(names):
            self.searchCodeComboBox.insertItem(i + 1, name)


class SensitiveDataWindow(DataGridWindow):
    def __init__(self):
        columns = dict(zip(
            ['id',  'sensitive_name', 'content', 'origin', 'create_time'],
            ['ID',  '敏感类型', '敏感内容', 'URL/FILE来源', '创建时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents,
                        QHeaderView.ResizeMode.Stretch, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents]
        super().__init__(table=TABLES.Sensitives.value, columns=columns, column_modes=column_modes)

    def custom_ui(self):
        self.searchCodeLabel.setText('敏感类型')
        names = [SENSITIVE_NAME.URL.value, SENSITIVE_NAME.IDCARD.value, SENSITIVE_NAME.KEYWORD.value]
        for i, name in enumerate(names):
            self.searchCodeComboBox.insertItem(i + 1, name)


class WhiteListDataWindow(DataGridWindow):
    def __init__(self, white_type='domain'):
        columns = dict(zip(
            ['id', 'ioc', 'desc', 'create_time'],
            ['ID', '内容', '描述', '创建时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents]
        db_where = 'white_type="%s"' % white_type
        super().__init__(table=TABLES.WhiteList.value, columns=columns, init_where=db_where, column_modes=column_modes)

    def custom_ui(self):
        self.searchCodeLabel.hide()
        self.searchCodeComboBox.hide()
        self.searchBtn.hide()
