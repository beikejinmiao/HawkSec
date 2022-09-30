#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
import shutil
from queue import Queue
from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from conf.paths import CRAWL_METRIC_PATH, EXTRACT_METRIC_PATH, DOWNLOADS
from libs.enums import SENSITIVE_FLAG, TABLES
from libs.pysqlite import Sqlite
from libs.client.downloader import WebCrawlDownloader
from libs.client.sftp import SSHSession
from modules.interaction.extractor import TextExtractor
from modules.interaction.persistence import DbPersistence
from utils.mixed import urlsite
from libs.logger import logger

browser_protocols = ('http', 'https', 'ftp')
support_protocols = ('http', 'https', 'ftp', 'sftp')


class TaskManager(QObject):
    expend_time_signal = pyqtSignal(float)

    def __init__(self, target, flags, keywords=None, protocol=None, auth_config=None):
        super().__init__()
        self.path_queue = Queue(10000)
        self.db_queue = Queue(10000)
        #
        self.protocol = None
        proto_candidates = re.findall(r'(\w+)://', target)  # https://  http://  ftp://  sftp://
        # 优先使用链接中的协议
        if len(proto_candidates) >= 1:
            proto = proto_candidates[0].lower()
            if proto in browser_protocols:
                self.protocol = proto
        if not self.protocol:
            self.protocol = protocol
        if self.protocol not in support_protocols:
            raise Exception('protocol of \'%s\' is not supported')
        #
        self.target = target
        if not re.match(r'^\w+://', self.target):
            self.target = self.protocol + '://' + self.target
        #
        if isinstance(flags, (list, type)) and len(flags) > 0:
            self.sensitive_flags = list(flags)
        else:
            raise ValueError('sensitive flag must be list or tuple, and can not be empty.')
        self._keywords = keywords
        #
        self.auth_config = auth_config
        self.extractor = self.__init_extractor()
        self.crawler = self.__init_crawler()
        self.persistencer = DbPersistence(db_queue=self.db_queue)
        #
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self._emit_expend_time)
        self._expend_time = 0.0
        self._start_time = time.time()

    def __init_crawler(self):
        client = None
        if self.protocol in browser_protocols:
            hsts = True if self.protocol == 'https' else False
            client = WebCrawlDownloader(self.target, hsts=hsts, extractor=self.extractor,
                                        path_queue=self.path_queue, db_queue=self.db_queue)
        elif self.protocol == 'sftp':
            if not isinstance(self.auth_config, dict) or 'password' not in self.auth_config:
                raise ValueError('ssh auth config is empty or has not password.')
            client = SSHSession(self.target,
                                port=self.auth_config.get('port', 22),
                                username=self.auth_config.get('username', 'root'),
                                password=self.auth_config['password'],
                                remote_root=self.auth_config.get('path', '/tmp'),
                                path_queue=self.path_queue, db_queue=self.db_queue)
        return client

    def __init_extractor(self):
        site = urlsite(self.target).reg_domain
        return TextExtractor(sensitive_flags=self.sensitive_flags, keywords=self._keywords,
                             path_queue=self.path_queue, db_queue=self.db_queue, website=site)

    def start(self):
        # 进程
        # ps_crawl = Process(target=self.crawler.run, name='crawl')
        # ps_extract = Process(target=self.extractor.extfrom_queue, name='extract')
        # while True:
        #     time.sleep(60)
        # ps_crawl.join()
        # ps_extract.join()

        # 线程
        self.crawler.start()
        self.extractor.start()
        self.persistencer.start()
        self._start_time = time.time()

    def terminate(self):
        self.crawler.terminate()
        self.extractor.terminate()
        self.persistencer.terminate()
        logger.info('%s' % '='*50)

    def _emit_expend_time(self):
        self._expend_time = time.time() - self._start_time
        self.expend_time_signal.emit(self._expend_time)
        
    @staticmethod
    def clear():
        # TODO 清空文件会导致GUI日志线程无法读取内容
        # if os.path.exists(LOG_FILEPATH):
        #     with open(LOG_FILEPATH, 'w') as fopen:
        #         fopen.write('')
        if os.path.exists(CRAWL_METRIC_PATH):
            os.remove(CRAWL_METRIC_PATH)
        if os.path.exists(EXTRACT_METRIC_PATH):
            os.remove(EXTRACT_METRIC_PATH)
        if os.path.exists(DOWNLOADS):
            shutil.rmtree(DOWNLOADS)
        os.makedirs(DOWNLOADS)
        #
        sqlite = Sqlite()
        sqlite.truncate([TABLES.CrawlStat.value, TABLES.Extractor.value, TABLES.Sensitives.value])
        sqlite.close()
        logger.info('成功清除历史数据')


if __name__ == '__main__':
    manager = TaskManager('https://www.ncut.edu.cn/', flags=[SENSITIVE_FLAG.URL, SENSITIVE_FLAG.IDCARD])
    # manager = TaskManager('106.13.202.41', protocol='sftp',
    #                       flags=[SensitiveType.URL, SensitiveType.IDCARD],
    #                       auth_config={'port': 61001, 'username': 'root', 'password': ''})
    try:
        manager.start()
    except KeyboardInterrupt:
        pass
