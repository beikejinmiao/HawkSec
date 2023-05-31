#!/usr/bin/env python
# -*- coding:utf-8 -*-
import yaml
from libs.singleton import Singleton
from conf.paths import CONF_PATH
from libs.logger import logger

_yaml_backup = {
    "timeout": 5,
    "ssh": {
        "password": None,
        "host": None,
        "port": 22,
        "username": "root",
        "path": "/tmp"
    },
    "target": "",
    "builtin_alexa": True,
    "protocol": "https",
    "charset": "auto",
    "metric": {
        "crawl_total": 0,
        "expend_time": "",
        "crawl_failed": 0,
        "origin_hit": 0,
        "start_time": "",
        "idcard_count": 0,
        "mobile_count": 0,
        "keyword_find": 0,
        "exturl_count": 0
    }
}


class Config(object):
    __metaclass__ = Singleton

    def __init__(self, filename):
        self.filename = filename
        self.cfg = dict()
        with open(filename, encoding='utf-8') as f:
            self.cfg = yaml.load(f, Loader=yaml.FullLoader)
        try:
            self.cfg['metric']['crawl_total']
        except:
            logger.warning('配置文件%s疑似损坏,恢复默认配置' % CONF_PATH)
            self.cfg = _yaml_backup

    def __setitem__(self, key, value):
        self.cfg[key] = value

    def __getitem__(self, item):
        return self.cfg[item]

    def __delitem__(self, key):
        del self.cfg[key]

    def get(self, key, default=None):
        if key not in self.cfg:
            return default
        return self.cfg[key]

    def save(self):
        with open(self.filename, "w") as f:
            yaml.dump(self.cfg, f)


configure = Config(CONF_PATH)
