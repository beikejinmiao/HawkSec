#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
import shutil
import tldextract
from queue import Empty
from collections.abc import Iterable
from PyQt6.QtCore import pyqtSignal
from libs.timer import timer
from libs.regex import img, video, executable, archive
from libs.pysqlite import Sqlite
from libs.enums import TABLES
from libs.enums import SENSITIVE_FLAG, sensitive_flag_name
from libs.thread import SuicidalQThread
from conf.paths import EXTRACT_METRIC_PATH
from utils.filedir import traverse
from tools.unzip import unpack
from tools.textract.automatic import extract as textract
from libs.regex import find_ioc, is_valid_ip, is_gov_edu
from utils.idcard import find_idcard
from modules.action.metric import ExtractMetric
from libs.logger import logger


LOCAL_ZIP_PATH_FLAG = '.unpack'   # 压缩文件解压后本地路径标志


class TextExtractor(SuicidalQThread):
    finished = pyqtSignal()

    def __init__(self, root=None, sensitive_flags=None, keywords=None, queue=None):
        super().__init__()

        if not root:
            self.files = dict()
        else:
            local_files = self.__get_files(root)
            # key:local file path,   value: remote file path or url
            self.files = dict(zip(local_files, [None for i in range(len(local_files))]))
        #
        self.regex_keyword = None
        if keywords is not None and len(keywords) > 0:
            self.regex_keyword = re.compile(r'(%s)' % '|'.join(keywords), re.I)
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
        self.sqlite = None      # sqlite不能跨线程使用,在线程内部run方法内初始化
        self._white_domain = set()
        self._white_url_file = set()
        self.__load_whitelist()
        #
        self.db_rows = {
            TABLES.Extractor.value: list(),
            TABLES.Sensitives.value: list(),
        }

    def __get_files(self, root):
        # 递归遍历所有本地文件路径
        local_files = list()
        if isinstance(root, (str, bytes)):
            if not os.path.exists(root):
                return local_files
            if os.path.isdir(root):
                local_files = traverse(root)
            else:
                local_files.append(root)
        elif isinstance(root, Iterable):
            for item in root:
                local_files.extend(self.__get_files(item))
        return local_files

    def __load_whitelist(self):
        sqlite = Sqlite()
        records = sqlite.select('SELECT ioc FROM %s WHERE white_type="domain"' % TABLES.WhiteList.value)
        for record in records:
            self._white_domain.add(record[0])
        records = sqlite.select('SELECT ioc FROM %s WHERE white_type="file"' % TABLES.WhiteList.value)
        for record in records:
            self._white_url_file.add(record[0])
        sqlite.close()

    # @timer(1, 1)      # 定时器线程会导致任务结束时还有剩余数据未插入
    def _sync2db(self):
        for table in self.db_rows:
            self.sqlite.insert_many(table, self.db_rows[table])
            self.db_rows[table] = list()

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
        if not self.regex_keyword:
            matches.extend(self.regex_keyword.findall(text))
        return matches

    def extract(self, text, local_path=None, origin=''):
        """
        :param text:        文件文本提取结果
        :param local_path:  本地文件路径
        :param origin:      网页URL、文件URL、SFTP远程文件路径
        :return:
        """
        result = dict()
        for flag in self.sensitive_flags:
            # 只在网页中提取提取外链,下载的文件中默认不提取
            if flag == SENSITIVE_FLAG.URL and local_path is not None:
                continue
            candidates = self.__funcs[flag](text)
            if len(candidates) > 0:
                self.sensitives[flag]['find'] += len(candidates)
                candidates = set(candidates)
                result[flag] = candidates
                self.sensitives[flag]['content'] = self.sensitives[flag]['content'] | candidates
        # 针对压缩文件,解压后的路径已发生变化,重新拼接来源地址
        if local_path is not None and local_path not in self.files \
                and LOCAL_ZIP_PATH_FLAG in local_path and origin:
            # 示例 http://1.1.1.1/test.zip    >>   http://1.1.1.1/test.zip.unpack/file_in.txt
            origin = origin + local_path[local_path.index(LOCAL_ZIP_PATH_FLAG):]
        #
        for flag, values in result.items():
            sensitive_name = sensitive_flag_name[flag].value
            self.db_rows[TABLES.Extractor.value].append({
                'origin': self.files.get(local_path, origin),       # 保存远程文件路径或者URL
                'sensitive_type': flag, 'sensitive_name': sensitive_name,
                'content': ', '.join(values), 'count': len(values),
            })
            for value in values:
                self.db_rows[TABLES.Sensitives.value].append({
                    'content': value, 'origin': self.files.get(local_path, origin),
                    'sensitive_type': flag, 'sensitive_name': sensitive_name,
                })

        if len(result) > 0:
            self._sync2db()
            if origin is not None:
                self.results[origin] = result
        return result

    def __extract_file(self, local_path, origin=None):
        if img.match(local_path) or video.match(local_path) or executable.match(local_path):
            return
        self.extract(textract(local_path), local_path=local_path, origin=origin)

    def __extract_dir(self, folder, origin=None):
        for local_path in traverse(folder):
            self.__extract_file(local_path, origin=origin)

    def load2extract(self, local_path, origin=None):
        """
        暂不支持自动遍历目录解析,如有需求请在初始化时通过root参数传入
        """
        if archive.match(local_path):
            self.counter['archive'] += 1
            dstdir = local_path + LOCAL_ZIP_PATH_FLAG
            unpack(local_path, dstdir=dstdir)
            self.__extract_dir(dstdir, origin=origin)
            shutil.rmtree(dstdir, ignore_errors=True)
        else:
            self.__extract_file(local_path, origin=origin)

    def extfrom_root(self):
        for local_path in self.files:
            self.load2extract(local_path)
        return self.results

    def extfrom_queue(self):
        # 无法根据queue是否empty自动退出(如果处理快于下载导致queue多数时间为空)
        while True:
            # local_path = self.queue.get(block=True)     # 阻塞至项目可得到
            try:
                local_path, remote_path = self.queue.get(block=False)      # 可停止的线程不能阻塞
                if local_path == 'END':
                    break
                self.files[local_path] = remote_path
                self.counter['que_get'] = self.counter.get('que_get', 0) + 1
                self.load2extract(local_path, origin=remote_path)
                os.remove(local_path)
            except Empty:
                time.sleep(1)

    def run(self):
        self.sqlite = Sqlite()
        # self.add_thread(self._sync2db())
        self.add_thread(self._dump_metric())
        if self.queue is not None:
            self.extfrom_queue()
        else:
            self.extfrom_root()
        self.sqlite.close()
        # time.sleep(2)     # 等待写入数据库结束(当sync2db是在定时器线程异步运行时)
        logger.info('敏感内容提取任务结束')
        # 发送结束信号
        self.finished.emit()

