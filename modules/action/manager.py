#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
from queue import Queue
from conf.paths import CRAWL_METRIC_PATH, EXTRACT_METRIC_PATH, LOG_FILEPATH
from libs.enums import SENSITIVE_FLAG, TABLES
from libs.pysqlite import Sqlite
from libs.client.downloader import WebCrawlDownloader
from libs.client.sftp import SSHSession
from modules.action.extractor import TextExtractor
from libs.logger import logger

browser_protocols = ('http', 'https', 'ftp')
support_protocols = ('http', 'https', 'ftp', 'sftp')


class TaskManager(object):
    def __init__(self, target, flags, keywords=None, protocol=None, auth_config=None):
        self.queue = Queue(100000)
        #
        self.target = target
        self.protocol = None
        proto_candidates = re.findall(r'(\w+)://', self.target)  # https://  http://  ftp://  sftp://
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
        if isinstance(flags, (list, type)) and len(flags) > 0:
            self.sensitive_flags = list(flags)
        else:
            raise ValueError('sensitive flag must be list or tuple, and can not be empty.')
        self._keywords = keywords
        #
        self.auth_config = auth_config
        self.extractor = self.__init_extractor()
        self.crawler = self.__init_crawler()

    def __init_crawler(self):
        client = None
        if self.protocol in browser_protocols:
            hsts = True if self.protocol == 'https' else False
            if not re.match(r'^\w+://', self.target):
                self.target = self.protocol + '://' + self.target
            client = WebCrawlDownloader(self.target, hsts=hsts, extractor=self.extractor, queue=self.queue)
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
        return TextExtractor(queue=self.queue, sensitive_flags=self.sensitive_flags, keywords=self._keywords)

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

    def terminate(self):
        self.crawler.terminate()
        self.extractor.terminate()
        logger.info('%s' % '='*50)

    @staticmethod
    def clear():
        sqlite = Sqlite()
        sqlite.truncate([TABLES.CrawlStat.value, TABLES.Extractor.value, TABLES.Sensitives.value])
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
    manager = TaskManager('https://www.ncut.edu.cn/', flags=[SENSITIVE_FLAG.URL, SENSITIVE_FLAG.IDCARD])
    # manager = TaskManager('106.13.202.41', protocol='sftp',
    #                       flags=[SensitiveType.URL, SensitiveType.IDCARD],
    #                       auth_config={'port': 61001, 'username': 'root', 'password': ''})
    try:
        manager.start()
    except KeyboardInterrupt:
        pass
