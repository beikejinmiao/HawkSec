#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from libs.enums import TABLES
from libs.pysqlite import Sqlite
from PyQt6.QtCore import QThread, pyqtSignal


class CrawlExtProgress(QThread):
    progress = pyqtSignal(dict)

    def __init__(self, extractor=None):
        super().__init__()
        self.sqlite = None
        self.extractor = extractor
        #
        self.terminated = False

    def run(self):
        # sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.
        # The object was created in thread id 4936 and this is thread id 6760.
        if self.sqlite is None:
            self.sqlite = Sqlite()
        while not self.terminated:
            time.sleep(2)
            #
            sql = 'SELECT count(*) FROM `{table}` ' \
                  'UNION ALL ' \
                  'SELECT count(*) FROM `{table}` WHERE resp_code=-1'.format(table=TABLES.CrawlStat.value)
            results = self.sqlite.select(sql)
            stat = {'crawled': results[0][0], 'failed': results[1][0]}
            if self.extractor is not None:
                stat.update({
                    'hit': len(self.extractor.results),
                    'external_url': len(self.extractor.sensitives['external_url']),
                    'idcard': len(self.extractor.sensitives['idcard']),
                    'keyword': len(self.extractor.sensitives['keyword']),
                })
            self.progress.emit(stat)

    def stop(self):
        self.terminated = True

