#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
import shutil
import tldextract
import threading
from queue import Empty
from libs.timer import timer
from libs.regex import img, video, executable, archive
from libs.pysqlite import Sqlite
from libs.enums import TABLES
from libs.enums import SensitiveType
from conf.paths import EXTRACT_METRIC_PATH
from utils.filedir import traverse
from tools.unzip import unpack
from tools.textract.automatic import extract as textract
from libs.regex import find_ioc, is_valid_ip, is_gov_edu
from utils.idcard import find_idcard
from modules.action.metric import ExtractMetric
from libs.logger import logger


class TextExtractor(threading.Thread):
    def __init__(self, root=None, sensitive_flags=None, queue=None):
        super().__init__()
        self.files = list()
        if isinstance(root, (list, tuple)):
            self.files = list(root)
        elif root and os.path.exists(root):
            if os.path.isdir(root):
                self.files = traverse(root)
            else:
                self.files.append(root)
        #
        self._white_domain = dict()
        self._keywords = list()
        self.queue = queue
        self.sensitive_flags = sensitive_flags
        self.results = dict()
        self.terminated = False
        #
        self.counter = {
            'archive': 0,
            'doc': 0,
            'others': 0,
        }
        self.sensitives = {
            'external_url': set(),
            'idcard': set(),
            'keyword': list(),
        }
        self.metric = ExtractMetric()
        #
        self.sqlite = None
        self.db_records = list()
        self.db_record_ix = 0

    @timer(2, 4)
    def _records2db(self):
        # sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.
        # The object was created in thread id 4936 and this is thread id 6760.
        if self.sqlite is None:
            self.sqlite = Sqlite()
        left = self.db_record_ix
        right = len(self.db_records)
        self.sqlite.insert_many(TABLES.Extractor.value, self.db_records[left:right])
        self.db_record_ix = right

    @timer(2, 1)
    def _dump_metric(self):
        self.metric.external_url = len(self.sensitives['external_url'])
        self.metric.idcard = len(self.sensitives['idcard'])
        self.metric.keyword = len(self.sensitives['keyword'])
        self.metric.origin_hit = len(self.results)
        self.metric.dump(EXTRACT_METRIC_PATH)

    def external_url(self, text):
        candidates = set()
        for item in find_ioc(text):
            if is_valid_ip(item):
                continue
            ext = tldextract.extract(item)
            reg_domain = ext.registered_domain.lower()
            if is_gov_edu(reg_domain) or reg_domain in self._white_domain:
                continue
            candidates.add(item)
        return list(candidates)

    @staticmethod
    def idcard(text):
        return find_idcard(text)

    def keyword(self, text):
        matches = list()
        for word in self._keywords:
            if len(re.findall(word, text)) > 0:
                matches.append(word)
        return matches

    def extract(self, text, origin=None):
        result = dict()
        if origin and re.match(r'^http[s]://', origin):
            # 只在网页中提取提取外链,下载的文件中不提取
            if SensitiveType.URL in self.sensitive_flags:
                candidates = self.external_url(text)
                if len(candidates) > 0:
                    result['external_url'] = candidates
                    self.sensitives['external_url'].union(set(candidates))
                    self.db_records.append({'origin': origin, 'sensitive_type': SensitiveType.URL.value,
                                            'result': ', '.join(candidates), 'count': len(candidates)})
        if SensitiveType.IDCARD in self.sensitive_flags:
            candidates = self.idcard(text)
            if len(candidates) > 0:
                result['idcard'] = candidates
                self.sensitives['idcard'].union(set(candidates))
                self.db_records.append({'origin': origin, 'sensitive_type': SensitiveType.IDCARD.value,
                                        'result': ', '.join(candidates), 'count': len(candidates)})
        if SensitiveType.KEYWORD in self.sensitive_flags:
            candidates = self.keyword(text)
            if len(candidates) > 0:
                result['keyword'] = candidates
                self.sensitives['keyword'].extend(candidates)
                self.db_records.append({'origin': origin, 'sensitive_type': SensitiveType.KEYWORD.value,
                                        'result': ', '.join(candidates), 'count': len(candidates)})
        if origin is not None and len(result) > 0:
            self.results[origin] = result
        return result

    def __extract_file(self, filepath):
        if img.match(filepath) or video.match(filepath) or executable.match(filepath):
            return
        self.extract(textract(filepath), origin=filepath)

    def __extract_dir(self, folder):
        for filepath in traverse(folder):
            self.__extract_file(filepath)

    def load2extract(self, filepath):
        """
        暂不支持自动遍历目录解析,如有需求请在初始化时通过root参数传入
        """
        if archive.match(filepath):
            self.counter['archive'] += 1
            dstdir = filepath + '.unpack'
            unpack(filepath, dstdir=dstdir)
            self.__extract_dir(dstdir)
            shutil.rmtree(dstdir, ignore_errors=True)
        else:
            self.__extract_file(filepath)

    def extfrom_root(self):
        results = dict()
        for filepath in self.files:
            if self.terminated:
                break
            #
            self.load2extract(filepath)
        return results

    def extfrom_queue(self):
        # 无法根据queue是否empty自动退出(如果处理快于下载导致queue多数时间为空)
        while not self.terminated:
            # filepath = self.queue.get(block=True)     # 阻塞至项目可得到
            try:
                filepath = self.queue.get(block=False)      # 可停止的线程不能阻塞
                self.counter['que_get'] = self.counter.get('que_get', 0) + 1
                self.load2extract(filepath)
                os.remove(filepath)
            except Empty:
                time.sleep(0.2)

    def run(self):
        self._records2db()
        self._dump_metric()
        if self.queue is not None:
            self.extfrom_queue()
        else:
            self.extfrom_root()
        logger.info('敏感内容提取任务%s' % '终止' if self.terminated else '完成')

    def stop(self):
        self.terminated = True
