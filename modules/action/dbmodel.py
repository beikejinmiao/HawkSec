#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt6.QtCore import Qt
from conf.paths import DB_PATH
from libs.pysqlite import Sqlite


class QueryModel(QSqlQueryModel):
    def data(self, index, role=None):
        # 表格数据居中显示
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
            # return Qt.AlignmentFlag.AlignLeft
        return super().data(index, role=role)


class TablePageModel(object):
    def __init__(self, table, columns):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(DB_PATH)
        self.db_where = None
        self.sqlite = Sqlite()

        # 当前页
        self.cur_page = 1
        # 每页记录数
        self.page_record = 10
        # 总页数
        self.total_page = 0
        # 总记录数
        self.total_record = 0
        # 跳转页数
        self.switch_page = self.cur_page
        #
        self.table = table
        self.columns = columns
        if isinstance(self.columns, dict):
            # key:   表字段名
            # value: 表字段中文名(展示用)
            self._columns = list(self.columns.keys())
        else:
            self._columns = columns
        self.__columns = ','.join(self._columns)
        #
        self.__init_state()

    def __init_state(self):
        self.query_model = QueryModel()
        if not self.db.isOpen():
            self.db.open()
        #
        self.update_total_count()
        self.limit_query(start_index=0)
        if isinstance(self.columns, dict):
            for i, name in enumerate(self.columns.values()):
                self.query_model.setHeaderData(i, Qt.Orientation.Horizontal, name)

    def update_total_count(self):
        # 默认最多返回256行
        # https://stackoverflow.com/questions/42286016/qsqlrelationaltablemodel-only-populates-first-256-records
        # sql = 'SELECT %s FROM `%s`' % (self.__columns, self.table)
        # self.query_model.setQuery(sql, self.db)
        # self.total_record = self.query_model.rowCount()
        self.total_record = self.sqlite.count(self.table, where=self.db_where)
        self.total_page = math.ceil(self.total_record / self.page_record)

    def update_ui_state(self):
        pass

    def limit_query(self, start_index=0, limit=None):
        if not limit:
            limit = self.page_record
        # columns不支持自定义,需全程保持一致,否则表格字段定义不生效
        # if not columns:
        #     columns = self.__columns
        # elif isinstance(columns, (list, tuple)):
        #     columns = ','.join(columns)
        sql = 'SELECT %s FROM `%s` %s ORDER BY `id` DESC LIMIT %d,%d' % \
              (self.__columns, self.table, '' if not self.db_where else 'WHERE '+self.db_where, start_index, limit)
        self.query_model.setQuery(sql, self.db)

    def query_page(self, page=None):
        if not page or page < 1:
            page = self.cur_page
        start_index = (page - 1) * self.page_record
        self.limit_query(start_index=start_index)
        self.update_ui_state()

    def on_prev_page(self):
        self.cur_page -= 1
        self.query_page()

    def on_next_page(self):
        self.cur_page += 1
        self.query_page()

    def on_switch_page(self):
        self.cur_page = self.switch_page
        self.query_page()

    def close_db(self):
        if self.db.isOpen():
            self.db.close()
        self.sqlite.close()

