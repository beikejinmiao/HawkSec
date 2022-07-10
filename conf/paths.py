#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
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
if stage == 'exe':
    if Platform == SYSTEM.WINDOWS or Platform == SYSTEM.DARWIN:
        DUMP_HOME = os.path.join(os.path.expanduser('~'), WORK_NAME)        # C:\\Users\\mozi\\hawksec
    elif Platform == SYSTEM.LINUX:
        DUMP_HOME = os.path.join('/tmp', WORK_NAME)
if not os.path.exists(DUMP_HOME):
    os.mkdir(DUMP_HOME)
DOWNLOADS = os.path.join(DUMP_HOME, 'downloads')
if not os.path.exists(DOWNLOADS):
    os.mkdir(DOWNLOADS)




