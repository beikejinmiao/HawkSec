#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import wget
import time
import threading
import traceback
from queue import Full
from collections import Counter
from urllib.parse import urlparse
from libs.timer import timer
from libs.regex import img, video, executable
from libs.client.crawler import Spider
from libs.pysqlite import Sqlite
from libs.enums import TABLES
from conf.paths import DUMP_HOME, DOWNLOADS
from modules.action.extractor import TextExtractor
from libs.logger import logger


class Downloader(threading.Thread):
    def __init__(self, out_dir=DOWNLOADS, queue=None):
        super().__init__()
        #
        self.out_dir = out_dir
        self.queue = queue
        self.terminated = False
        #
        self.counter = {
            'success': 0,
            'failed': 0,
            'ignored': 0,
        }
        #
        self.db = None
        self.db_records = list()
        self.db_record_ix = 0

    def _put_queue(self, local_path):
        if self.queue is None:
            return
        # 当queue长度大于1000时等待消费端处理,避免堆积过多导致占用过多磁盘空间
        while self.queue.qsize() > 1000:
            if not self.terminated:
                logger.debug('Queue size greater than 1000, sleep 1s.')
                time.sleep(1)
        try:
            # self.queue.put(local_path, block=True)        # 阻塞至有空闲槽可用
            self.queue.put(local_path, block=False)         # 可停止的线程不能阻塞
        except Full:
            time.sleep(0.2)
        self.counter['que_put'] = self.counter.get('que_put', 0) + 1

    @timer(120, 120)
    def _log_stats(self):
        logger.info('Downloader count stats: %s' % json.dumps(self.counter))

    @timer(2, 4)
    def _records2db(self):
        if self.db is None:
            self.db = Sqlite()
        left = self.db_record_ix
        right = len(self.db_records)
        self.db.insert_many(TABLES.CrawlStat.value, self.db_records[left:right])
        self.db_record_ix = right

    def crawling(self):
        pass

    def downloads(self):
        pass

    def close(self):
        pass

    def run(self):
        self._log_stats()
        self._records2db()
        if not self.terminated:
            self.crawling()
        if not self.terminated:
            self.downloads()
        self.close()
        logger.info('Downloader task terminated')

    def stop(self):
        self.terminated = True


class WebFileDownloader(Downloader):
    def __init__(self, urls=None, urls_file=None, out_dir=DOWNLOADS, queue=None):
        super().__init__(out_dir=out_dir, queue=queue)

        # if not urls and not urls_file:
        #     raise ValueError('下载地址和地址文件不能同时为空')
        self.urls = list()
        if urls_file:
            with open(urls_file) as fopen:
                _urls_ = fopen.readlines()
            self.urls.extend(_urls_)
        if urls:
            self.urls.extend(list(urls))

    def download(self, url):
        path = urlparse(url.strip()).path
        suffix = None
        # 默认不下载图片和可执行文件
        if img.match(path) or video.match(path) or executable.match(path):
            self.counter['ignored'] += 1
        try:
            filename = wget.download(url, out=self.out_dir)
            suffix = path.split('.')[-1].lower()
            self.counter['success'] += 1
            # 将下载文件的本地路径放入队列中
            self._put_queue(os.path.join(self.out_dir, filename))
            logger.info('Download: %s' % url)
        except:
            self.counter['failed'] += 1
            # UnicodeError: encoding with 'idna' codec failed (UnicodeError: label empty or too long)
            logger.error(traceback.format_exc())
            logger.error('Download Error: %s' % url)
        return suffix

    def downloads(self):
        suffixes = list()
        for url in self.urls:
            if self.terminated:
                break
            #
            suffix = self.download(url)
            if suffix is not None:
                suffixes.append(suffix)
        # 统计文件类型数量
        file_types = dict(Counter(suffixes).most_common())
        self.counter['file_type'] = file_types
        logger.info('Download done.\nDownloader count stats: %s' % json.dumps(self.counter))
        logger.info('File Types:\n %s' % json.dumps(file_types, indent=4))


class WebCrawlDownloader(Spider, WebFileDownloader):
    def __init__(self, start_url,
                 same_site=True,
                 headers=None,
                 timeout=10,
                 hsts=False,
                 out_dir=DOWNLOADS,
                 sensitive_flags=None,
                 queue=None):
        #
        Spider.__init__(self, start_url, same_site=same_site, headers=headers, timeout=timeout, hsts=hsts)
        WebFileDownloader.__init__(self, out_dir=out_dir, queue=queue)
        self.sensitive_flags = sensitive_flags
        self.extractor = TextExtractor(sensitive_flags=self.sensitive_flags)
        self._file_urls_archive = open(os.path.join(DUMP_HOME, 'fileurls.txt'), 'w')

    def crawling(self):
        for resp in self.scrape():
            if self.terminated:
                break
            #
            self.db_records.append({'origin': resp.url, 'resp_code': resp.status_code})
            if resp.filename:
                # 文件链接单独处理,网页爬取完毕后再下载
                self._file_urls_archive.write(resp.url + '\n')
                continue
            if resp.status_code >= 400:
                self.counter['failed'] += 1
            elif resp.status_code == 200:
                self.counter['success'] += 1
            # 1.解析网页中的敏感内容
            if resp.html_text:
                self.extractor.extract(resp.html_text, origin=resp.url)
        # 2. 下载文件解析敏感内容
        self.urls = list(self.file_urls.keys())

    def close(self):
        self.session.close()
        if not self._file_urls_archive.closed:
            self._file_urls_archive.close()
        logger.info('Downloader成功关闭Web Session和文件资源')
