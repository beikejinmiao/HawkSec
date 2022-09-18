#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import json
import traceback
from json.decoder import JSONDecodeError
from PyQt6.QtCore import QThread, pyqtSignal
from conf.paths import CRAWL_METRIC_PATH, EXTRACT_METRIC_PATH
from libs.logger import logger


class AbstractMetric(object):
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def dump(self, path):
        with open(path, 'w', encoding='utf-8') as fout:
            json.dump(self.__dict__, fout, indent=4)


class CrawlMetric(AbstractMetric):
    def __init__(self, crawl_total=0, crawl_success=0, crawl_failed=0, crawl_ignored=0,
                 file_total=0, file_success=0, file_failed=0, file_ignored=0, queue_put=-1):
        self.crawl_total = crawl_total
        self.crawl_success = crawl_success
        self.crawl_failed = crawl_failed
        self.crawl_ignored = crawl_ignored
        self.file_total = file_total
        self.file_success = file_success
        self.file_failed = file_failed
        self.file_ignored = file_ignored
        self.queue_put = queue_put


class ExtractMetric(AbstractMetric):
    def __init__(self, external_url_find=0, external_url_count=0,
                 idcard_find=0, idcard_count=0,
                 keyword_find=0, keyword_count=0,
                 origin_hit=0, queue_get=-1):
        self.exturl_find = external_url_find
        self.exturl_count = external_url_count
        self.idcard_find = idcard_find
        self.idcard_count = idcard_count
        self.keyword_find = keyword_find
        self.keyword_count = keyword_count
        self.origin_hit = origin_hit
        self.queue_get = queue_get


class QCrawlExtProgress(QThread):
    progress = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    @staticmethod
    def metric():
        stat = None
        try:
            stat = dict()
            with open(CRAWL_METRIC_PATH, encoding='utf-8') as fopen:
                stat = json.load(fopen)
            with open(EXTRACT_METRIC_PATH, encoding='utf-8') as fopen:
                stat.update(json.load(fopen))
        except FileNotFoundError:
            pass
        except JSONDecodeError:
            # 由于多线程同时读取同一个文件导致错误
            # json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
            pass
        except:
            logger.error(traceback.format_exc())
        return stat

    def run(self):
        while True:
            time.sleep(1)
            #
            metric = self.metric()
            if metric:
                self.progress.emit(metric)



