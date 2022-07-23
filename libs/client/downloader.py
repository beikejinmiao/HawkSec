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
from conf.paths import DUMP_HOME, DOWNLOADS, CRAWL_METRIC_PATH
from modules.action.metric import CrawlMetric
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
        self.metric = CrawlMetric()
        #
        self.sqlite = None
        self.db_rows = list()
        self.__db_row_ix = 0    # 用于记录已插入数据库中的self.db_rows最后一条索引位置

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
        if self.metric.queue_put < 0:
            self.metric.queue_put = 0
        self.metric.queue_put += 1

    @timer(120, 120)
    def _log_stats(self):
        logger.info('爬虫客户端Metric统计: %s' % self.metric)

    @timer(2, 4)
    def _sync2db(self):
        if self.sqlite is None:
            self.sqlite = Sqlite()
        left = self.__db_row_ix
        right = len(self.db_rows)
        self.sqlite.insert_many(TABLES.CrawlStat.value, self.db_rows[left:right])
        self.__db_row_ix = right

    @timer(2, 1)
    def _dump_metric(self):
        self.metric.dump(CRAWL_METRIC_PATH)

    def crawling(self):
        pass

    def downloads(self):
        pass

    def close(self):
        pass

    def run(self):
        self._log_stats()
        self._sync2db()
        self._dump_metric()
        if not self.terminated:
            self.crawling()
        if not self.terminated:
            self.downloads()
        self.close()
        logger.info('爬虫客户端任务%s' % '终止' if self.terminated else '完成')

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
        self.metric.file_total += 1
        if img.match(path) or video.match(path) or executable.match(path):
            self.metric.file_ignored += 1
        try:
            filename = wget.download(url, out=self.out_dir)
            self.db_rows.append({'origin': url, 'resp_code': 0, 'desc': 'Success'})
            suffix = path.split('.')[-1].lower()
            self.metric.file_success += 1
            # 将下载文件的本地路径放入队列中
            self._put_queue(os.path.join(self.out_dir, filename))
            logger.info('Download: %s' % url)
        except Exception as e:
            self.metric.file_failed += 1
            self.db_rows.append({'origin': url, 'resp_code': -1, 'desc': str(e)})
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
        logger.info('下载%s' % '终止' if self.terminated else '完成')
        logger.info('爬虫客户端Metric统计: %s' % self.metric)
        logger.info('文件类型统计: %s' % json.dumps(file_types, indent=4))


class WebCrawlDownloader(Spider, WebFileDownloader):
    def __init__(self, start_url,
                 same_site=True,
                 headers=None,
                 timeout=10,
                 hsts=False,
                 out_dir=DOWNLOADS,
                 extractor=None,
                 queue=None):
        #
        Spider.__init__(self, start_url, same_site=same_site, headers=headers, timeout=timeout, hsts=hsts)
        WebFileDownloader.__init__(self, out_dir=out_dir, queue=queue)
        self.extractor = extractor
        self._file_urls_archive = open(os.path.join(DUMP_HOME, 'fileurls.txt'), 'w')

    def crawling(self):
        for resp in self.scrape():
            if self.terminated:
                break
            #
            if resp.filename:
                # 文件链接单独处理,网页爬取完毕后再下载
                self._file_urls_archive.write(resp.url + '\n')
                continue
            self.db_rows.append({'origin': resp.url, 'resp_code': resp.status_code, 'desc': resp.desc})
            self.metric.crawl_total += 1
            if resp.status_code == 200:
                self.metric.crawl_success += 1
            else:
                self.metric.crawl_failed += 1
            # 1.解析网页中的敏感内容
            if resp.html_text and self.extractor is not None:
                self.extractor.extract(resp.html_text, origin=resp.url)
        # 2. 下载文件解析敏感内容
        self.urls = list(self.file_urls.keys())
        logger.info('爬取URL%s' % '终止' if self.terminated else '完成')
        logger.info('爬虫客户端Metric统计: %s' % self.metric)
        logger.info('发现文件URL: %s个' % len(self.urls))

    def close(self):
        self.session.close()
        if not self._file_urls_archive.closed:
            self._file_urls_archive.close()
        logger.info('WebCrawler成功关闭Web Session和文件资源')
