#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
import shutil
import traceback
from urllib.parse import urlparse
from collections.abc import Iterable
from collections import namedtuple
from PyQt5.QtCore import pyqtSignal
from libs.timer import timer
from libs.regex import archive
from libs.pysqlite import Sqlite
from libs.enums import TABLES
from libs.enums import SENSITIVE_FLAG, sensitive_flag_name
from libs.thread import SuicidalQThread
from libs.filter import Alexa
from conf.paths import EXTRACT_METRIC_PATH
from utils.filedir import traverse
from tools.unzip import unpack
from tools.textract.automatic import extract as textract
from libs.regex import find_urls, is_gov_edu
from utils.idcard import find_idcard
from libs.web.page import page_info, page_a_href
from libs.web.url import normal_url, urlsite
from modules.interaction.metric import ExtractMetric
from modules.win.settings import setting
from libs.logger import logger


LOCAL_ZIP_PATH_FLAG = '.unpack'   # 压缩文件解压后本地路径标志


class TextExtractor(SuicidalQThread):
    Result = namedtuple('Result', ['flag', 'origin', 'content'])
    finished = pyqtSignal()
    cur_result = pyqtSignal(Result)
    metrics = pyqtSignal(ExtractMetric)

    def __init__(self, root=None, sensitive_flags=None, keywords=None, path_queue=None, db_queue=None, website=''):
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
            self.regex_keyword = re.compile(r'(%s)' % '|'.join(keywords))
        self.path_queue = path_queue
        self.db_queue = db_queue
        self.sensitive_flags = sensitive_flags
        self.website = website
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
        self._metric = ExtractMetric()
        #
        self.alexa = Alexa()
        self._white_domain = set()
        self._white_url_file = set()
        self.__load_whitelist()
        # 限制外链数量
        self.__ext_urlpath_limit = dict()

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

    def _put_db_queue(self, table, record):
        if self.db_queue is None:
            return
        self.db_queue.put((table, record), block=True)        # 阻塞至有空闲槽可用

    # 2022-07-29 15:14:32,146 - ERROR - file - timer.py:28 - Exception: Traceback (most recent call last):
    #   File "D:\PycharmProjects\HawkSec\libs\timer.py", line 26, in run
    #     self._target(*self._args, **self._kwargs)
    #   File "D:\PycharmProjects\HawkSec\modules\action\extractor.py", line 115, in _sync2db
    #     sqlite.insert_many(table, self.db_rows[table][left:right])
    #   File "D:\PycharmProjects\HawkSec\libs\pysqlite.py", line 54, in insert_many
    #     self.__cursor.executemany(stmt, values[i*win:min((i+1)*win, size)])
    # sqlite3.OperationalError: database is locked
    # @timer(1, 2)      # 定时器线程会导致任务结束时还有剩余数据未插入,需在主线程结束后等待一段时间
    # def _sync2db(self):
    #     sqlite = Sqlite()   # sqlite不能跨线程使用,在线程内部初始化
    #     for table in self.db_rows:
    #         left = self.__db_row_ix[table]
    #         right = len(self.db_rows[table])
    #         if right > left:
    #             sqlite.insert_many(table, self.db_rows[table][left:right])
    #             self.__db_row_ix[table] = right
    #     sqlite.close()

    def _update_metric(self):
        self._metric.exturl_count = len(self.sensitives[SENSITIVE_FLAG.URL]['content'])
        self._metric.idcard_count = len(self.sensitives[SENSITIVE_FLAG.IDCARD]['content'])
        self._metric.keyword_count = len(self.sensitives[SENSITIVE_FLAG.KEYWORD]['content'])
        self._metric.exturl_find = self.sensitives[SENSITIVE_FLAG.URL]['find']
        self._metric.idcard_find = self.sensitives[SENSITIVE_FLAG.IDCARD]['find']
        self._metric.keyword_find = self.sensitives[SENSITIVE_FLAG.KEYWORD]['find']
        self._metric.origin_hit = len(self.results)

    @timer(2, 2)
    def _dump_metric(self):
        self._update_metric()
        self._metric.dump(EXTRACT_METRIC_PATH)

    def external_url(self, text):
        candidates = set()
        for item in find_urls(text):
            # 过滤同站和白域名
            reg_domain = urlsite(item).reg_domain
            if reg_domain == '' or reg_domain == self.website:
                continue
            if is_gov_edu(reg_domain) or reg_domain in self._white_domain:
                continue
            if setting.builtin_alexa is True and reg_domain in self.alexa:
                continue
            # 同一个站点路径,只保存一条记录
            parts = urlparse(item)
            urlpath = "{0.scheme}://{0.netloc}{0.path}".format(parts)
            if urlpath in self.__ext_urlpath_limit:
                continue
            else:
                self.__ext_urlpath_limit[urlpath] = 1
            #
            candidates.add(normal_url(item))
        return list(candidates)

    @staticmethod
    def idcard(text):
        return find_idcard(text)

    def keyword(self, text):
        matches = list()
        if self.regex_keyword is not None:
            matches.extend(self.regex_keyword.findall(text))
        return matches

    def extract(self, text, local_path=None, origin=''):
        """
        :param text:        文件文本提取结果
        :param local_path:  本地文件路径
        :param origin:      网页URL、文件URL、SFTP远程文件路径
        :return:
        """
        if not text:
            return None
        #
        result = dict()
        try:
            for flag in self.sensitive_flags:
                # 只在网页中提取提取外链,下载的文件中默认不提取
                if flag == SENSITIVE_FLAG.URL and local_path is not None:
                    continue
                candidates = self.__funcs[flag](text)
                if len(candidates) > 0:
                    self.sensitives[flag]['find'] += len(candidates)
                    candidates = set(candidates)  # 本次发现的敏感内容
                    if flag == SENSITIVE_FLAG.KEYWORD:
                        candidates_new = candidates
                    else:
                        candidates_new = candidates - self.sensitives[flag]['content']      # 本次新发现的敏感内容
                    result[flag] = (candidates, candidates_new)
                    self.sensitives[flag]['content'] = self.sensitives[flag]['content'] | candidates
                    self.cur_result.emit(self.Result(flag=flag, origin=origin, content=','.join(candidates)))
            # 针对压缩文件,解压后的路径已发生变化,重新拼接来源地址
            if local_path is not None and local_path not in self.files \
                    and LOCAL_ZIP_PATH_FLAG in local_path and origin:
                # 示例 http://1.1.1.1/test.zip    >>   http://1.1.1.1/test.zip.unpack/file_in.txt
                origin = origin + local_path[local_path.index(LOCAL_ZIP_PATH_FLAG):]
            #
            for flag, values in result.items():
                sensitive_name = sensitive_flag_name[flag].value
                record = {
                    'origin': self.files.get(local_path, origin),                   # 保存远程文件路径或者URL
                    'sensitive_type': flag, 'sensitive_name': sensitive_name,
                    'content': ', '.join(values[0]), 'count': len(values[0]),       # 本次发现的敏感内容
                }
                self._put_db_queue(TABLES.Extractor.value, record)
                # 如果发现新外链，尝试从a标签中提取title，并尝试访问校验其返回码
                exturl_info = dict()
                if flag == SENSITIVE_FLAG.URL and len(values[1]) > 0:
                    exturl_info = page_a_href(text)
                    for url in values[1]:
                        resp = page_info(url)
                        # 1. 优先使用url的返回结果中的title
                        # 2. 若title中文数量小于等于2，则尝试取a标签中的title内容
                        title = resp.title
                        if len(re.findall('[\u4e00-\u9fa5]', title)) <= 2:
                            _a_title = exturl_info.get(url, '')
                            if _a_title:
                                title = _a_title
                        exturl_info[url] = (title, '%s %s' % (resp.status_code, resp.desc))
                #
                for value in values[1]:                                             # 本次新发现的敏感内容
                    record = {
                        'content': value, 'origin': self.files.get(local_path, origin),
                        'sensitive_type': flag, 'sensitive_name': sensitive_name
                    }
                    record['content_name'], record['desc'] = exturl_info.get(value, ('', ''))
                    self._put_db_queue(TABLES.Sensitives.value, record)
            #
            self._update_metric()
            self.metrics.emit(self._metric)
            #
            if len(result) > 0 and origin:
                # self._sync2db()
                self.results[origin] = result
        except Exception as e:
            logger.warning('解析敏感内容失败: %s' % origin)
            logger.warning(repr(e))
            # logger.error(traceback.format_exc())
        return result

    def __extract_file(self, local_path, origin=None):
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
            local_path, remote_path = self.path_queue.get(block=True)      # 阻塞至项目可得到
            if local_path == 'END':
                break
            self.files[local_path] = remote_path
            self.counter['que_get'] = self.counter.get('que_get', 0) + 1
            try:
                self.load2extract(local_path, origin=remote_path)
            except Exception as e:
                logger.error(str(e) + ': %s' % local_path)
            # 处理删除文件时的错误
            try_count = 3
            while try_count > 0:
                try_count -= 1
                try:
                    if os.path.exists(local_path):
                        # PermissionError: [WinError 32] 另一个程序正在使用此文件，进程无法访问
                        # 由于wps关闭文件需要一定时间，所以删除失败时尝试等待0.5秒再次删除
                        os.remove(local_path)
                except:
                    time.sleep(0.5)
            if os.path.exists(local_path):
                logger.warning('删除文件失败: %s' % local_path)

    def run(self):
        # self.add_thread(self._sync2db())
        # self.add_thread(self._dump_metric())
        # 捕获内部异常,防止异常导致无法发送结束信号
        try:
            if self.path_queue is not None:
                self.extfrom_queue()
            else:
                self.extfrom_root()
            self._put_db_queue('END', None)
        except SystemExit:
            pass
        except:
            logger.error('敏感内容提取任务异常终止, 错误详情:')
            logger.error(traceback.format_exc())
        time.sleep(3)     # 等待写入数据库结束
        # 发送结束信号
        self.finished.emit()
        logger.info('敏感内容提取任务结束')

