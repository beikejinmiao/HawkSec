#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import threading
# from multiprocessing import Queue, Process
from queue import Queue
from conf.paths import CRAWL_METRIC_PATH, EXTRACT_METRIC_PATH, LOG_FILEPATH
from libs.enums import SensitiveType, TABLES
from libs.pysqlite import Sqlite
from libs.client.downloader import WebCrawlDownloader
from libs.client.sftp import SSHSession
from modules.action.extractor import TextExtractor
from libs.logger import logger


class TaskManager(object):
    def __init__(self, target, flags, protocol=None, auth_config=None):
        self.queue = Queue(100000)
        #
        self.target = target
        self.protocol = protocol
        if not self.protocol:
            candidates = re.findall(r'(\w+)://', self.target)     # https://  http://  ftp://  sftp://
            if len(candidates) >= 1:
                self.protocol = candidates[0].lower()
        if not self.protocol:
            raise Exception('can not confirm the protocol.')
        #
        if isinstance(flags, (list, type)) and len(flags) > 0:
            self.sensitive_flags = list(flags)
        else:
            raise ValueError('sensitive flag must be list or tuple, and can not be empty.')
        #
        self.auth_config = auth_config
        self.crawler = self.__init_crawler()
        self.extractor = self.__init_extractor()

    def __init_crawler(self):
        client = None
        if self.protocol in ('http', 'https', 'ftp'):
            hsts = True if self.protocol == 'https' else False
            client = WebCrawlDownloader(self.target, hsts=hsts, queue=self.queue,
                                        sensitive_flags=self.sensitive_flags)
        elif self.protocol == 'sftp':
            if not isinstance(self.auth_config, dict) or 'password' not in self.auth_config:
                raise ValueError('ssh auth config is empty or has not password.')
            client = SSHSession(self.target,
                                port=self.auth_config.get('port', 22),
                                username=self.auth_config.get('username', 'root'),
                                password=self.auth_config['password'],
                                remote_root=self.auth_config.get('path', '/tmp'),
                                queue=self.queue)
        return client

    def __init_extractor(self):
        return TextExtractor(queue=self.queue, sensitive_flags=self.sensitive_flags)

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
        logger.info('%s Manager started %s' % ('=' * 18, '=' * 18))

    def stop(self):
        self.crawler.stop()
        self.extractor.stop()
        self.crawler.join()
        self.extractor.join()
        logger.info('%s Manager stopped %s' % ('=' * 18, '=' * 18))

    @staticmethod
    def clear():
        sqlite = Sqlite()
        sqlite.truncate(TABLES.CrawlStat.value)
        sqlite.truncate(TABLES.Extractor.value)
        sqlite.close()
        # TODO 清空文件会导致GUI日志线程无法读取内容
        # if os.path.exists(LOG_FILEPATH):
        #     with open(LOG_FILEPATH, 'w') as fopen:
        #         fopen.write('')
        if os.path.exists(CRAWL_METRIC_PATH):
            os.remove(CRAWL_METRIC_PATH)
        if os.path.exists(EXTRACT_METRIC_PATH):
            os.remove(EXTRACT_METRIC_PATH)
        logger.info('成功清除历史数据')


if __name__ == '__main__':
    manager = TaskManager('https://www.ncut.edu.cn/', flags=[SensitiveType.URL, SensitiveType.IDCARD])
    # manager = TaskManager('106.13.202.41', protocol='sftp',
    #                       flags=[SensitiveType.URL, SensitiveType.IDCARD],
    #                       auth_config={'port': 61001, 'username': 'root', 'password': ''})
    try:
        manager.start()
    except KeyboardInterrupt:
        pass
