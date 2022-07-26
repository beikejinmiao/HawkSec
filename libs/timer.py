#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import threading
import traceback
from libs.pysqlite import Sqlite
from libs.thread import SuicidalThread
from libs.logger import logger


class SimpleTimer(SuicidalThread):
    def __init__(self, delay, period, target, *args, **kwargs):
        super().__init__()
        self.delay = delay
        self.period = period
        self._target = target
        self._args = tuple(args)
        self._kwargs = dict(kwargs)

    def run(self):
        if self.delay and self.delay > 0:
            time.sleep(self.delay)

        while True:
            try:
                self._target(*self._args, **self._kwargs)
            except:
                logger.error("Exception: {0}".format(traceback.format_exc()))
            time.sleep(self.period)


class SqliteTimer(threading.Thread):
    def __init__(self, delay, period, target, *args, **kwargs):
        super().__init__()
        self.delay = delay
        self.period = period
        self._target = target
        self._args = tuple(args)
        self._kwargs = dict(kwargs)
        #
        self._stop_event = threading.Event()
        self.sqlite = None

    def terminate(self):
        self._stop_event.set()

    def terminated(self):
        return self._stop_event.is_set()

    def run(self):
        if self.delay and self.delay > 0:
            time.sleep(self.delay)
        # sqlite不能跨线程使用
        # sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.
        # The object was created in thread id 4936 and this is thread id 6760.
        self.sqlite = Sqlite()
        while True:
            try:
                if self.terminated():
                    break
                self._target(self.sqlite, *self._args, **self._kwargs)
            except:
                logger.error("Exception: {0}".format(traceback.format_exc()))
            # 使用事件方式停止线程,会导致线程延迟关闭,最多延迟self.period秒
            time.sleep(self.period)
        # 安全关闭sqlite
        self.sqlite.close()


def timer(delay, period, db_type=None):
    def decorate(func):
        def wrapper(*args, **kwargs):
            if db_type and db_type == 'sqlite':
                _timer = SqliteTimer(delay, period, func, *args, **kwargs)
            else:
                _timer = SimpleTimer(delay, period, func, *args, **kwargs)
            _timer.start()
            return _timer
        return wrapper
    return decorate


# SqliteTimer使用样例
# @timer(0, 2, db_type='sqlite')
# def task(sqlite):
#     print(sqlite.count(''))

