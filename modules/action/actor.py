#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
from libs.regex import img, video, executable, archive
from utils.filedir import traverse
from tools.unzip import unpack
from tools.textract.iparse import extract as textract
from libs.logger import logger


class TextExtractor(object):
    def __init__(self, root=None, queue=None):
        self.files = []
        if root and os.path.exists(root):
            if os.path.isdir(root):
                self.files = traverse(root)
            else:
                self.files.append(root)
        #
        self.queue = queue
        self.infos = dict()
        #
        self.counter = {
            'archive': 0,
            'doc': 0,
            'others': 0,
        }

    @staticmethod
    def __extract(root):
        results = dict()
        files = traverse(root)
        for filepath in files:
            textract(filepath)
        return results

    def extract(self):
        # 无法根据queue是否empty自动退出(如果处理快于下载导致queue多数时间为空)
        while True:
            filepath = self.queue.get(block=True)     # 阻塞至项目可得到
            self.counter['que_get'] = self.counter.get('que_get', 0) + 1
            if img.match(filepath) or video.match(filepath) or executable.match(filepath):
                continue
            if archive.match(filepath):
                self.counter['archive'] += 1
                dstdir = filepath + '.unpack'
                unpack(filepath, dstdir=dstdir)
                results = self.__extract(dstdir)
                shutil.rmtree(dstdir, ignore_errors=True)
            else:
                results = self.__extract(filepath)
            if results:
                self.infos.update(results)
            os.remove(filepath)






