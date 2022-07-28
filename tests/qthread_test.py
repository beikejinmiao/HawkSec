#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from libs.timer import timer
from libs.thread import SuicidalThread
from PyQt6.QtCore import QThread, pyqtSignal


class QTestThread(QThread):
    """
    测试QThread主线程terminate后普通子线程是否会自动停止
    """
    progress = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.count = 0

    @timer(0, 1)
    def timer_print(self):
        print(self.count)
        self.count += 1

    def run(self):
        # 启动定时器
        sub_th = self.timer_print()
        while True:
            time.sleep(1)
            print('main qthread sleep')

    @staticmethod
    def test():
        qth = QTestThread()
        qth.start()
        time.sleep(5)
        qth.terminate()
        print('terminate main qthread')
        # QThread主线程terminate后，子线程继续执行
        time.sleep(5)
        # QThread主线程退出后后，子线程自动退出


if __name__ == '__main__':
    QTestThread.test()



