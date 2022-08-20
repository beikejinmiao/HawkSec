#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import shutil
from pathlib import Path
from conf.config import Platform
from libs.enums import SYSTEM

stage = 'exe' if hasattr(sys, "_MEIPASS") else 'dev'

if stage == 'exe':
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    MAIN_HOME = sys._MEIPASS
    WORK_NAME = 'hawksec'  # 打包好后的exe目录名和结构已发生变化,根目录名是随机生成的
else:
    # 工作目录
    MAIN_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    # 工程名
    WORK_NAME = MAIN_HOME.split(os.sep)[-1].lower()  # hawksec

#
CONF_HOME = os.path.join(MAIN_HOME, 'conf')
TOOLS_HOME = os.path.join(MAIN_HOME, 'tools')
DUMP_HOME = os.path.join(MAIN_HOME, 'zdump')
USER_HOME = os.path.expanduser('~')
RUNTIME_HOME = os.path.join(USER_HOME, WORK_NAME)
PRIVATE_RESOURCE_HOME = os.path.join(MAIN_HOME, 'resources')
RUNTIME_RESOURCE_HOME = os.path.join(RUNTIME_HOME, 'resources')
if not os.path.exists(RUNTIME_RESOURCE_HOME):
    os.makedirs(RUNTIME_RESOURCE_HOME)

IMAGE_HOME = Path(os.path.join(PRIVATE_RESOURCE_HOME, 'image')).as_posix()

CONF_PATH = os.path.join(CONF_HOME, WORK_NAME+'.yaml')
DB_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'hawksec.db')
CRAWL_METRIC_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'crawl.metric.json')
EXTRACT_METRIC_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'extract.metric.json')
LOG_FILEPATH = os.path.join(DUMP_HOME, "%s.log" % WORK_NAME)
ALEXA_FILEPATH = os.path.join(PRIVATE_RESOURCE_HOME, 'alexa-top-30k.txt')

if stage == 'exe':
    LOG_FILEPATH = os.path.join(RUNTIME_HOME, "%s.log" % WORK_NAME)
    #
    runtime_paths = list()
    for path in [CONF_PATH, DB_PATH, CRAWL_METRIC_PATH, EXTRACT_METRIC_PATH]:
        runtime_path = os.path.join(RUNTIME_RESOURCE_HOME, os.path.basename(path))
        if os.path.exists(path) and not os.path.exists(runtime_path):
            shutil.copy(path, runtime_path)
        runtime_paths.append(runtime_path)
    CONF_PATH, DB_PATH, CRAWL_METRIC_PATH, EXTRACT_METRIC_PATH = tuple(runtime_paths)
    #
    if Platform == SYSTEM.WINDOWS or Platform == SYSTEM.DARWIN:
        DUMP_HOME = os.path.join(RUNTIME_HOME, 'zdump')        # C:\\Users\\mozi\\hawksec\\zdump
    elif Platform == SYSTEM.LINUX:
        DUMP_HOME = os.path.join('/tmp', WORK_NAME)
#
DOWNLOADS = os.path.join(DUMP_HOME, 'downloads')
if not os.path.exists(DOWNLOADS):
    os.makedirs(DOWNLOADS)




