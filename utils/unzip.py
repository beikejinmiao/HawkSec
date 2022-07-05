#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import platform
import shutil
import rarfile
from py7zr import pack_7zarchive, unpack_7zarchive
from conf.paths import TOOLS_HOME

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
if platform.system().lower() == 'windows':
    UNRAR_PATH = os.path.join(TOOLS_HOME, 'unrar', 'unrar.win.exe')


def unrar(path):
    rarfile.UNRAR_TOOL = UNRAR_PATH
    rar = rarfile.RarFile(path)
    dest_dir = path + '.unpack'
    with rar as rf:
        rf.extractall(dest_dir)


def unpack(path):
    filename = os.path.basename(path)
    if filename.endswith('.rar'):
        unrar(path)
    elif re.match(r'.*\.(zip|7z|tar|tar\.bz2|tar\.gz|tar\.xz|tbz2|tgz|txz)$', filename, re.I):
        dest_dir = path + '.unpack'
        # shutil.ReadError: xxx.zip is not a zip file
        shutil.unpack_archive(path, dest_dir)
