#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pybloom_live import BloomFilter
from conf.paths import ALEXA_BLOOM_FILTER_PATH, WHITE_DOMAIN_FILE_PATH
from libs.singleton import Singleton


class Filter(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.filter = None
        self._load_filter()

    def __contains__(self, value):
        return self.contains(value)

    def _load_filter(self):
        pass

    def contains(self, source):
        if (self.filter is not None) and (source in self.filter):
            return True
        return False


class Alexa(Filter):
    def _load_filter(self):
        with open(ALEXA_BLOOM_FILTER_PATH, 'rb') as fopen:
            self.bloom_filter = BloomFilter.fromfile(fopen)
        #
        self.filter = set()
        with open(WHITE_DOMAIN_FILE_PATH) as fopen:
            for line in fopen.readlines():
                self.filter.add(line.strip('\r\n '))

    def contains(self, source):
        if source in self.bloom_filter or source in self.filter:
            return True
        return False

