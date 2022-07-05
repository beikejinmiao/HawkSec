#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import yaml
from libs.singleton import Singleton
from conf.paths import WORK_NAME, CONF_HOME

LINUX = sys.platform.startswith('linux')
PY3 = sys.version_info[0] == 3


def system_config_dir():
    r"""Return the system-wide config dir (full path).
    - Linux: /etc/hawksec
    """
    path = None
    if LINUX:
        path = '/etc'

    if path is None:
        path = ''
    else:
        path = os.path.join(path, WORK_NAME)

    return path


class Config(object):
    __metaclass__ = Singleton

    def __init__(self, filename):
        self.filename = filename
        self.cfg = dict()
        with open(filename, encoding='utf-8') as f:
            self.cfg = yaml.load(f, Loader=yaml.FullLoader)

    def __setitem__(self, key, value):
        self.cfg[key] = value

    def __getitem__(self, item):
        return self.cfg[item]

    def __delitem__(self, key):
        del self.cfg[key]

    def save(self):
        with open(self.filename, "w") as f:
            yaml.dump(self.cfg, f)


configure = Config(os.path.join(CONF_HOME, WORK_NAME+'.yaml'))
