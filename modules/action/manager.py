#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from multiprocessing import Queue, Process
from libs.enums import SensitiveFLAG
from libs.client.crawler import Spider
from libs.client.downloader import WebCrawlDownloader
from libs.client.sftp import SSHSession
from modules.action.actor import TextExtractor
from libs.logger import logger


class TaskManager(object):
    def __init__(self, target, protocol='http', flags=0):
        self.queue = Queue(100000)
        #
        self.target = target
        self.protocol = protocol
        self.sensitive_flags = flags
        #
        self.__init_env()

    def __init_env(self):
        if self.protocol in ('http', 'https', 'ftp'):
            hsts = True if self.protocol == 'https' else False
            if self.sensitive_flags == SensitiveFLAG.URL:
                self.client = Spider(self.target, hsts=hsts)
            elif self.sensitive_flags == SensitiveFLAG.URL | SensitiveFLAG.IDCARD:
                self.client = WebCrawlDownloader(self.target, hsts=hsts, queue=self.queue)
        elif self.protocol == 'sftp':
            self.client = SSHSession(self.target, queue=self.queue)
        #
        self.extractor = TextExtractor(queue=self.queue)

    def crawl(self):
        self.client.downloads()
        self.client.close()

    def extract(self):
        self.extractor.extract()

    def run(self):
        ps_crawl = Process(target=self.crawl, name='crawl')
        ps_extract = Process(target=self.extract, name='extract')
        ps_crawl.start()
        ps_extract.start()
        logger.info('start')
        while True:
            time.sleep(60)


if __name__ == '__main__':
    manager = TaskManager('')
    try:
        manager.run()
    except KeyboardInterrupt:
        pass
