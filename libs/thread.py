#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import inspect
import ctypes


# https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def force_kill(thread):
    _async_raise(thread.ident, SystemExit)


class SuicidalThread(threading.Thread):
    """
    有self-destroying倾向的线程
    """
    def __init__(self, daemon=True):
        super().__init__()
        self.daemon = daemon      # 默认随着父线程退出而退出
        self._sub_threads = list()

    def add_sub_thd(self, thread):
        if not isinstance(thread, threading.Thread):
            raise ValueError('%s is not a thread' % thread)
        self._sub_threads.append(thread)

    def cleanup(self):
        pass

    @staticmethod
    def safe_kill(thread):
        if not isinstance(thread, threading.Thread):
            return
        if not thread.is_alive():
            return
        # Kill线程之前尝试清理占用资源
        if isinstance(thread, SuicidalThread):
            thread.cleanup()
        force_kill(thread)

    def kill_all_sub(self):
        for thread in self._sub_threads:
            self.safe_kill(thread)

    def terminate(self):
        # 1. Kill所有子线程
        self.kill_all_sub()
        # 2. 自毁
        self.safe_kill(self)

