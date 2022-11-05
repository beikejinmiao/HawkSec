#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import traceback
from queue import Empty
from libs.pysqlite import Sqlite
from libs.thread import SuicidalThread
from libs.logger import logger


class DbPersistence(SuicidalThread):
    def __init__(self, db_queue=None):
        super().__init__()
        self.sqlite = None
        self.db_queue = db_queue
        self.db_rows = dict()
        self.__new_row_cnt = 0
        self.__pre_time = time.time()
        self.__cur_time = time.time()

    def run(self):
        if self.db_queue is None:
            return
        #
        self.sqlite = Sqlite()
        while True:
            try:
                table, record = self.db_queue.get(block=False)
                # 接收到结束标志将剩余数据存入数据库
                if table == 'END':
                    self.sync2db()
                    break
                #
                if table not in self.db_rows:
                    self.db_rows[table] = list()
                self.db_rows[table].append(record)
                #
                self.__new_row_cnt += 1
                if self.__new_row_cnt > 10 or (self.__cur_time - self.__pre_time) > 2:
                    # 数量超过10个或者时间超过2秒,同步数据至数据库
                    self.sync2db()
                    self.__new_row_cnt = 0
                    self.__pre_time = self.__cur_time
                    self.__cur_time = time.time()
            except Empty:
                time.sleep(1)
                self.__cur_time = time.time()
                if (self.__cur_time - self.__pre_time) > 2:
                    # 数量超过10个或者时间超过2秒,同步数据至数据库
                    self.sync2db()
                    self.__new_row_cnt = 0
                    self.__pre_time = self.__cur_time
        #
        self.sqlite.close()

    def sync2db(self):
        try:
            for table, rows in self.db_rows.items():
                if len(rows) > 0:
                    self.sqlite.insert_many(table, rows)
            self.db_rows.clear()
        except:
            logger.error(traceback.format_exc())

    # def cleanup(self):
    #     self.sqlite.close()

