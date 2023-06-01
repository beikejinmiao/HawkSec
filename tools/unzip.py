#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import shutil
import rarfile
from py7zr import pack_7zarchive, unpack_7zarchive
from conf.config import Platform
from conf.paths import TOOLS_HOME
from libs.logger import logger
from libs.enums import System
from utils.filedir import traverse


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
if Platform == System.WINDOWS:
    UNRAR_PATH = os.path.join(TOOLS_HOME, 'unrar', 'unrar.win.exe')


def unrar(filepath, dstdir=None):
    dstdir = filepath + '.unpack' if not dstdir else dstdir
    #
    rarfile.UNRAR_TOOL = UNRAR_PATH
    rar = rarfile.RarFile(filepath)
    with rar as rf:
        rf.extractall(dstdir)


def __unpack(filepath, dstdir):
    if re.match(r'.*\.rar$', filepath, re.I):
        # 在解压前打印日志,避免解压过程卡死导致无法正确打印日志
        logger.info("解压: '%s'" % filepath)
        unrar(filepath, dstdir=dstdir)
    else:
        # shutil.ReadError: xxx.zip is not a zip file
        logger.info("解压: '%s'" % filepath)
        shutil.unpack_archive(filepath, dstdir)


def unpack(filepath, dstdir=None, depth=2):
    """
    解压压缩包文件(目前不支持xz/gz)

    注意：解压zip文件时,实际使用的是zipfile.py,有中文乱码情况
         解决办法：搜索cp437, 全部替换为gbk.
    :return:
    """
    if depth is None:
        depth = 16  # 默认最大解压深度设置为16
    if depth <= 0:
        return
    if not re.match(r'.*\.(rar|zip|7z|tar|tar\.bz2|tar\.gz|tar\.xz|tbz2|tgz|txz)$', filepath, re.I):
        return
    #
    dstdir = filepath + '.unpack' if not dstdir else dstdir
    __unpack(filepath, dstdir)
    for sub_filepath in traverse(dstdir):
        unpack(sub_filepath, depth=depth-1)


if __name__ == '__main__':
    unpack(r'D:\var\depth3.7z', depth=None)
