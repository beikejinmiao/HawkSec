#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import shutil
import tldextract
from libs.regex import img, video, executable, archive
from libs.enums import SensitiveType
from utils.filedir import traverse
from tools.unzip import unpack
from tools.textract.automatic import extract as textract
from libs.regex import find_ioc, is_valid_ip, is_gov_edu
from utils.idcard import find_idcard


class TextExtractor(object):
    def __init__(self, root=None, sensitive_flags=None, queue=None):
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
        #
        self.counter = {
            'archive': 0,
            'doc': 0,
            'others': 0,
        }

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
                result['external_url'] = self.external_url(text)
        if SensitiveType.IDCARD in self.sensitive_flags:
            result['idcard'] = self.idcard(text)
        if SensitiveType.KEYWORD in self.sensitive_flags:
            result['keyword'] = self.keyword(text)
        if origin is not None:
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
            self.load2extract(filepath)
        return results

    def extfrom_queue(self):
        # 无法根据queue是否empty自动退出(如果处理快于下载导致queue多数时间为空)
        while True:
            filepath = self.queue.get(block=True)     # 阻塞至项目可得到
            self.counter['que_get'] = self.counter.get('que_get', 0) + 1
            self.load2extract(filepath)
            os.remove(filepath)


