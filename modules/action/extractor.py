#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
import shutil
import tldextract
from queue import Empty
from libs.timer import timer
from libs.regex import img, video, executable, archive
from libs.pysqlite import Sqlite
from libs.enums import TABLES
from libs.enums import SENSITIVE_FLAG, sensitive_flag_name
from libs.thread import SuicidalThread
from conf.paths import EXTRACT_METRIC_PATH
from utils.filedir import traverse
from tools.unzip import unpack
from tools.textract.automatic import extract as textract
from libs.regex import find_ioc, is_valid_ip, is_gov_edu
from utils.idcard import find_idcard
from modules.action.metric import ExtractMetric
from libs.logger import logger


class TextExtractor(SuicidalThread):
    def __init__(self, root=None, sensitive_flags=None, keywords=None, queue=None):
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
        self._keywords = set() if keywords is None else set(keywords)
        self.queue = queue
        self.sensitive_flags = sensitive_flags
        self.results = dict()           # key:origin,  value:敏感内容类型以及content列表
        #
        self.counter = {
            'archive': 0,
            'doc': 0,
            'others': 0,
        }
        self.sensitives = {
            SENSITIVE_FLAG.URL: {'content': set(), 'find': 0},
            SENSITIVE_FLAG.IDCARD: {'content': set(), 'find': 0},
            SENSITIVE_FLAG.KEYWORD: {'content': set(), 'find': 0},
        }
        self.__funcs = {
            SENSITIVE_FLAG.URL: self.external_url,
            SENSITIVE_FLAG.IDCARD: self.idcard,
            SENSITIVE_FLAG.KEYWORD: self.keyword,
        }
        self.metric = ExtractMetric()
        #
        self.sqlite = Sqlite()
        self._white_domain = set()
        self._white_file = set()
        self.__load_whitelist()
        #
        self.db_rows = {
            TABLES.Extractor.value: list(),
            TABLES.Sensitives.value: list(),
        }
        self.__db_row_ix = {
            TABLES.Extractor.value: 0,
            TABLES.Sensitives.value: 0,
        }

    def __load_whitelist(self):
        records = self.sqlite.select('SELECT ioc FROM %s WHERE white_type="domain"' % TABLES.WhiteList.value)
        for record in records:
            self._white_domain.add(record[0])
        records = self.sqlite.select('SELECT ioc FROM %s WHERE white_type="file"' % TABLES.WhiteList.value)
        for record in records:
            self._white_file.add(record[0])

    @timer(2, 4)
    def _sync2db(self):
        sqlite = Sqlite()
        for table in self.db_rows:
            left = self.__db_row_ix[table]
            right = len(self.db_rows[table])
            sqlite.insert_many(table, self.db_rows[table][left:right])
            self.__db_row_ix[table] = right
        sqlite.close()

    @timer(2, 1)
    def _dump_metric(self):
        self.metric.external_url_count = len(self.sensitives[SENSITIVE_FLAG.URL]['content'])
        self.metric.idcard_count = len(self.sensitives[SENSITIVE_FLAG.IDCARD]['content'])
        self.metric.keyword_count = len(self.sensitives[SENSITIVE_FLAG.KEYWORD]['content'])
        self.metric.external_url_find = self.sensitives[SENSITIVE_FLAG.URL]['find']
        self.metric.idcard_find = self.sensitives[SENSITIVE_FLAG.IDCARD]['find']
        self.metric.keyword_find = self.sensitives[SENSITIVE_FLAG.KEYWORD]['find']
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
        for flag in self.sensitive_flags:
            if flag == SENSITIVE_FLAG.URL:
                if not (origin and re.match(r'^http[s]://', origin)):
                    # 只在网页中提取提取外链,下载的文件中不提取
                    continue
            candidates = self.__funcs[flag](text)
            if len(candidates) > 0:
                self.sensitives[flag]['find'] += len(candidates)
                candidates = set(candidates)
                result[flag] = candidates
                self.sensitives[flag]['content'] = self.sensitives[flag]['content'] | candidates

        for flag, values in result.items():
            sensitive_name = sensitive_flag_name[flag].value
            sensitive_flag = flag.value
            self.db_rows[TABLES.Extractor.value].append({
                'origin': origin,
                'sensitive_type': sensitive_flag, 'sensitive_name': sensitive_name,
                'content': ', '.join(values), 'count': len(values),
            })
            for value in values:
                self.db_rows[TABLES.Sensitives.value].append({
                    'content': value, 'origin': origin,
                    'sensitive_type': sensitive_flag, 'sensitive_name': sensitive_name,
                })

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
        for filepath in self.files:
            self.load2extract(filepath)
        return self.results

    def extfrom_queue(self):
        # 无法根据queue是否empty自动退出(如果处理快于下载导致queue多数时间为空)
        while True:
            # filepath = self.queue.get(block=True)     # 阻塞至项目可得到
            try:
                filepath = self.queue.get(block=False)      # 可停止的线程不能阻塞
                if filepath == 'END':
                    break
                self.counter['que_get'] = self.counter.get('que_get', 0) + 1
                self.load2extract(filepath)
                os.remove(filepath)
            except Empty:
                time.sleep(0.2)

    def run(self):
        self.add_sub_thd(self._sync2db())
        self.add_sub_thd(self._dump_metric())
        if self.queue is not None:
            self.extfrom_queue()
        else:
            self.extfrom_root()
        logger.info('敏感内容提取任务结束')
