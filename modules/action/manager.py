#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import time
from multiprocessing import Queue, Process
from libs.enums import SensitiveType
from libs.client.downloader import WebCrawlDownloader
from libs.client.sftp import SSHSession
from modules.action.actor import TextExtractor
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

    def crawl(self):
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
        client.run()

    def extract(self):
        extractor = TextExtractor(queue=self.queue, sensitive_flags=self.sensitive_flags)
        extractor.extfrom_queue()

    def start(self):
        ps_crawl = Process(target=self.crawl, name='crawl')
        ps_extract = Process(target=self.extract, name='extract')
        ps_crawl.start()
        ps_extract.start()
        logger.info('manager start')
        while True:
            time.sleep(60)

    def stop(self):
        pass


if __name__ == '__main__':
    manager = TaskManager('https://www.ncut.edu.cn/', flags=[SensitiveType.URL, SensitiveType.IDCARD])
    # manager = TaskManager('106.13.202.41', protocol='sftp',
    #                       flags=[SensitiveType.URL, SensitiveType.IDCARD],
    #                       auth_config={'port': 61001, 'username': 'root', 'password': ''})
    try:
        manager.start()
    except KeyboardInterrupt:
        pass
