#!/usr/bin/env python
# -*- coding:utf-8 -*-
from conf.paths import ALEXA_FILEPATH
from libs.singleton import Singleton
from utils.filedir import reader


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
        self.filter = dict()
        for line in reader(ALEXA_FILEPATH):
            if line.startswith("#"):
                continue
            self.filter[line] = None

