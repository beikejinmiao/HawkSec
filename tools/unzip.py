#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import platform
import shutil
import rarfile
from py7zr import pack_7zarchive, unpack_7zarchive
from conf.config import PLATFORM
from conf.paths import TOOLS_HOME
from libs.logger import logger
from libs.enums import SYSTEM


# https://bbs.huaweicloud.com/blogs/180864
# register file format at first.
shutil.register_archive_format('7zip',
                               pack_7zarchive,
                               description='7zip archive')
shutil.register_unpack_format('7zip',
                              ['.7z'],
                              unpack_7zarchive,
                              description='7zip archive')


UNRAR_PATH = os.path.join(TOOLS_HOME, 'unrar', 'unrar.linux')
if PLATFORM == SYSTEM.WINDOWS:
    UNRAR_PATH = os.path.join(TOOLS_HOME, 'unrar', 'unrar.win.exe')


def unrar(filepath):
    rarfile.UNRAR_TOOL = UNRAR_PATH
    rar = rarfile.RarFile(filepath)
    dest_dir = filepath + '.unpack'
    with rar as rf:
        rf.extractall(dest_dir)


def unpack(filepath, dstdir=None):
    filename = os.path.basename(filepath)
    if filename.endswith('.rar'):
        unrar(filepath)
    elif re.match(r'.*\.(zip|7z|tar|tar\.bz2|tar\.gz|tar\.xz|tbz2|tgz|txz)$', filename, re.I):
        dstdir = filepath + '.unpack' if not dstdir else dstdir
        # shutil.ReadError: xxx.zip is not a zip file
        shutil.unpack_archive(filepath, dstdir)
    logger.info("Unpack: '%s'" % filepath)
