#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import traceback
from collections import Counter
from urllib.parse import urlparse
from PyQt5.QtCore import pyqtSignal
from libs.timer import timer
from libs.client.crawler import Spider, UrlFileInfo
from libs.pyaml import configure
from libs.pysqlite import Sqlite
from libs.enums import TABLES
from libs.thread import SuicidalQThread
from libs.web import pywget
from conf.paths import DUMP_HOME, DOWNLOADS, CRAWL_METRIC_PATH
from modules.interaction.metric import CrawlMetric
from libs.logger import logger


class Downloader(SuicidalQThread):

    metrics = pyqtSignal(CrawlMetric)

    def __init__(self, out_dir=DOWNLOADS, path_queue=None, db_queue=None):
        super().__init__()
        #
        self.out_dir = out_dir
        self.path_queue = path_queue
        self.db_queue = db_queue
        #
        self._metric = CrawlMetric()
        self._white_url_file = set()
        self.__load_whitelist()
        #
        # self.sqlite = None
        # self.db_rows = list()
        # self.__db_row_ix = 0    # 用于记录已插入数据库中的self.db_rows最后一条索引位置

    def _put_path_queue(self, msg):
        if self.path_queue is None:
            return
        self.path_queue.put(msg, block=True)         # 可停止的线程不能阻塞

    def _put_db_queue(self, table, record):
        if self.db_queue is None:
            return
        self.db_queue.put((table, record), block=True)        # 阻塞至有空闲槽可用

    def __load_whitelist(self):
        sqlite = Sqlite()
        records = sqlite.select('SELECT ioc FROM %s WHERE white_type="file"' % TABLES.WhiteList.value)
        for record in records:
            self._white_url_file.add(record[0])
        sqlite.close()

    @timer(120, 120)
    def _log_stats(self):
        logger.info('爬虫客户端Metric统计: %s' % self._metric)

    # # TODO 终止线程时sqlite报错,后续无法重现
    # #  2022-07-26 10:05:34,016 - ERROR - file - timer.py:26 - Exception: Traceback (most recent call last):
    # #    File "libs\timer.py", line 24, in run
    # #    File "libs\client\downloader.py", line 61, in _sync2db
    # #    File "libs\pysqlite.py", line 52, in insert_many
    # #  SystemExit
    # # @timer(1, 2, db_type='sqlite')  # 使用SqliteTimer无法访问类对象资源
    # @timer(1, 2)
    # def _sync2db(self):
    #     # TODO 定时器线程内部初始化sqlite,永远无法关闭sqlite连接
    #     if self.sqlite is None:
    #         self.sqlite = Sqlite()
    #     left = self.__db_row_ix
    #     right = len(self.db_rows)
    #     if right > left:
    #         self.sqlite.insert_many(TABLES.CrawlStat.value, self.db_rows[left:right])
    #         self.__db_row_ix = right

    @timer(2, 2)
    def _dump_metric(self):
        self._metric.dump(CRAWL_METRIC_PATH)

    def crawling(self):
        pass

    def downloads(self):
        pass

    def run(self):
        self.add_thread(self._log_stats())
        # self.add_thread(self._sync2db())
        # self.add_thread(self._dump_metric())
        try:
            self.crawling()
        except SystemExit:
            return
        except:
            logger.error('爬取任务异常终止, 错误详情:')
            logger.error(traceback.format_exc())
        logger.info('开始下载文件')
        try:
            self.downloads()
        except SystemExit:
            pass
        except:
            logger.error('文件下载任务异常终止, 错误详情:')
            logger.error(traceback.format_exc())
        logger.info('文件下载结束')
        try:
            self.cleanup()
        except:
            logger.error(traceback.format_exc())
        logger.info('爬虫客户端任务结束')
        logger.info('爬虫Metric统计: %s' % self._metric)


class WebFileDownloader(Downloader):
    def __init__(self, urls=None, url_file=None, out_dir=DOWNLOADS, path_queue=None, db_queue=None):
        super().__init__(out_dir=out_dir, path_queue=path_queue, db_queue=db_queue)

        self.file_urls = dict()
        if urls:
            for url in urls:
                url = url.strip('\r\n ')
                self.file_urls[url] = UrlFileInfo(url=url, url_from='parameter', filename=url_file(url))
        if url_file:
            with open(url_file) as fopen:
                for url in fopen.readlines():
                    url = url.strip('\r\n ')
                    self.file_urls[url] = UrlFileInfo(url=url, url_from=url_file, filename=url_file(url))

    def download(self, url):
        # 过滤白名单
        if url in self._white_url_file:
            return None
        #
        path = urlparse(url.strip()).path
        suffix = None
        self._metric.file_total += 1
        self._metric.crawl_total += 1
        logger.info('Download: %s' % url)
        url_info = self.file_urls[url]
        try:
            fileinfo = pywget.download(url, out=self.out_dir)
            record = {'origin': url,
                      'origin_name': fileinfo.filename, 'origin_from': url_info.url_from,
                      'resp_code': fileinfo.status_code, 'desc': fileinfo.desc}
            self._put_db_queue(TABLES.CrawlStat.value, record)
            # self.db_rows.append(record)
            if fileinfo.filepath is not None:
                suffix = path.split('.')[-1].lower()
                self._metric.file_success += 1
                self._metric.crawl_success += 1
                # 将下载文件的本地路径和文件URL放入队列中
                self._put_path_queue((fileinfo.filepath, url))
            else:
                self._metric.file_failed += 1
                self._metric.crawl_failed += 1
                logger.error('Download Error(%s %s): %s' % (fileinfo.status_code, fileinfo.desc, url))
        except Exception as e:
            self._metric.file_failed += 1
            self._metric.crawl_failed += 1
            record = {'origin': url,
                      'origin_name': url_info.filename, 'origin_from': url_info.url_from,
                      'resp_code': -1, 'desc': type(e).__name__}
            self._put_db_queue(TABLES.CrawlStat.value, record)
            # self.db_rows.append(record)
            # UnicodeError: encoding with 'idna' codec failed (UnicodeError: label empty or too long)
            logger.error(traceback.format_exc())
            logger.error('Download Error: %s' % url)
        return suffix

    def downloads(self):
        suffixes = list()
        for url in self.file_urls:
            suffix = self.download(url)
            if suffix is not None:
                suffixes.append(suffix)
            self.metrics.emit(self._metric)
        self._put_path_queue(('END', None))
        # 统计文件类型数量
        file_types = dict(Counter(suffixes).most_common())
        logger.info('文件类型统计: %s' % json.dumps(file_types))


class WebCrawlDownloader(Spider, WebFileDownloader):
    def __init__(self, start_url,
                 limited_sites=None,
                 headers=None,
                 hsts=False,
                 out_dir=DOWNLOADS,
                 extractor=None,
                 path_queue=None,
                 db_queue=None):
        #
        timeout = configure.get('timeout', 5)
        Spider.__init__(self, start_url, limited_sites=limited_sites, headers=headers, timeout=timeout, hsts=hsts)
        WebFileDownloader.__init__(self, out_dir=out_dir, path_queue=path_queue, db_queue=db_queue)
        self.extractor = extractor
        self._file_urls_archive = open(os.path.join(DUMP_HOME, 'fileurls.txt'), 'w')

    def crawling(self):
        for resp in self.scrape():
            try:
                if resp.filename:
                    # 文件链接单独处理,网页爬取完毕后再下载
                    # UnicodeEncodeError: 'gbk' codec can't encode character '\xe6' in position 74: illegal multibyte sequence
                    self._file_urls_archive.write(resp.url + '\n')
                    continue
                # 非文件链接不记录URL来源网页地址
                record = {'origin': resp.url, 'origin_name': resp.title,
                          'resp_code': resp.status_code, 'desc': resp.desc}
                self._put_db_queue(TABLES.CrawlStat.value, record)
                self._metric.crawl_total += 1
                # 解析网页中的敏感内容
                if resp.text and self.extractor is not None:
                    self.extractor.extract(resp.text, origin=resp.url)
            except:
                logger.error(resp.url)
                logger.error(traceback.format_exc())
            finally:
                resp.text = None  # 一定要清除text内容,否则内存将不可控的增长
            #
            if 0 < resp.status_code < 400:
                self._metric.crawl_success += 1
            else:
                self._metric.crawl_failed += 1
            self.metrics.emit(self._metric)
        # 2. 下载文件解析敏感内容
        self.file_urls = self._file_urls
        logger.info('爬取URL结束')
        logger.info('爬虫客户端Metric统计: %s' % self._metric)
        logger.info('发现文件URL: %s个' % len(self.file_urls))

    def cleanup(self):
        self.session.close()
        if not self._file_urls_archive.closed:
            self._file_urls_archive.close()
        logger.info('WebCrawler成功关闭Web Session和文件资源')
