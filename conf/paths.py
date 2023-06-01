#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import shutil
from pathlib import Path
from conf.config import Platform, RuntimeEnv
from libs.enums import System

# 打包好后的exe目录名和结构已发生变化,根目录名是随机生成的
# 不能从路径中获取,需直接定义
WORK_NAME = 'hawksec'   # MAIN_HOME.split(os.sep)[-1].lower()  # hawksec
USER_HOME = os.path.expanduser('~')
RUNTIME_HOME = os.path.join(USER_HOME, WORK_NAME)

if RuntimeEnv == 'exe':
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    MAIN_HOME = sys._MEIPASS
    #
    if Platform == System.WINDOWS:
        DUMP_HOME = 'C:\\HawkSec'
    elif Platform == System.DARWIN:
        DUMP_HOME = os.path.join(USER_HOME, 'HawkSec')
    else:
        DUMP_HOME = os.path.join('/tmp', 'HawkSec')
else:
    # 工作目录
    MAIN_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    #
    DUMP_HOME = os.path.join(MAIN_HOME, 'zdump')

#
CONF_HOME = os.path.join(MAIN_HOME, 'conf')
TOOLS_HOME = os.path.join(MAIN_HOME, 'tools')
PRIVATE_RESOURCE_HOME = os.path.join(MAIN_HOME, 'resources')
RUNTIME_RESOURCE_HOME = os.path.join(RUNTIME_HOME, 'resources')
if not os.path.exists(RUNTIME_RESOURCE_HOME):
    os.makedirs(RUNTIME_RESOURCE_HOME)
#
CONF_PATH = os.path.join(CONF_HOME, WORK_NAME+'.yaml')
#
IMAGE_HOME = Path(os.path.join(PRIVATE_RESOURCE_HOME, 'image')).as_posix()
DB_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'hawksec.db')
CRAWL_METRIC_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'crawl.metric.json')
EXTRACT_METRIC_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'extract.metric.json')
WHITE_DOMAIN_FILE_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'whitedomain.txt')
ALEXA_BLOOM_FILTER_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'top-30k-sites.blm')
START_MOVIE_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'waitloading.mp4')

if RuntimeEnv == 'exe':
    runtime_paths = list()
    for path in [CONF_PATH, DB_PATH, CRAWL_METRIC_PATH, EXTRACT_METRIC_PATH]:
        runtime_path = os.path.join(RUNTIME_RESOURCE_HOME, os.path.basename(path))
        if os.path.exists(path) and not os.path.exists(runtime_path):
            shutil.copy(path, runtime_path)
        runtime_paths.append(runtime_path)
    CONF_PATH, DB_PATH, CRAWL_METRIC_PATH, EXTRACT_METRIC_PATH = tuple(runtime_paths)
#
LOG_FILEPATH = os.path.join(DUMP_HOME, "%s.log" % WORK_NAME)
#
DOWNLOADS = os.path.join(DUMP_HOME, 'downloads')
if not os.path.exists(DOWNLOADS):
    os.makedirs(DOWNLOADS)
#
LICENSE_PATH = os.path.join(USER_HOME, '.'+WORK_NAME+'.lic')
