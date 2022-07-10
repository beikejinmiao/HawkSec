#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import logging
import logging.config
from PyQt6 import QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal
from conf.paths import LOG_FILEPATH


class QTextEditLogger(logging.Handler):
    # https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt
    """
    Usage：
        import logging
        from libs.logger import QTextEditLogger, LOGGING_CONFIG

        self.logTextBox = QTextEditLogger(self.centralwidget)
        self.logTextBox.setFormatter(logging.Formatter(LOGGING_CONFIG['formatters']['default']['format']))
        logging.getLogger().addHandler(self.logTextBox)
        self.logTextBox.widget.setGeometry(QtCore.QRect(30, 170, 831, 211))
        self.logTextBox.widget.setObjectName("logTextBrowser")
    注意：
        1.子线程添加的日志会使GUI崩溃
        2.子进程无法访问该logger, 无法打印日志
    结论:
        在多线程和多进程环境中无法使用, 废弃
    """
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class QLogTailReader(QObject):
    # https://realpython.com/python-pyqt-qthread/
    # https://medium.com/@aliasav/how-follow-a-file-in-python-tail-f-in-python-bca026a901cf
    """
    QTextEditLogger的替代实现
    创建子线程读取日志文件, 将日志内容发送至GUI主线程, 由主线程添加至日志框
    """
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    @staticmethod
    def follow():
        with open(LOG_FILEPATH, 'r') as fopen:
            # seek the end of the file
            fopen.seek(0, os.SEEK_END)
            # start infinite loop
            while True:
                # read last line of file
                line = fopen.readline()
                # sleep if file hasn't been updated
                if not line:
                    time.sleep(0.5)
                    continue
                yield line

    def run(self):
        """Long-running task."""
        for line in self.follow():
            self.progress.emit(line.strip())
        self.finished.emit()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": "true",
    "formatters": {
        "short": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        },
        "default": {
            "class": "logging.Formatter",
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)s - %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": LOG_FILEPATH,
            "mode": "w+",
            "encoding": "utf-8"
        }
    },

    "loggers": {
        "console": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "file": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        }
    },

    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("file")


if __name__ == '__main__':
    for text in QLogTailReader.follow():
        print(text)

