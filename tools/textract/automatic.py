#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import traceback
import magic
from tika import parser as tikarser
from conf.config import Platform, TIKA_SERVER_ACTIVE
from libs.enums import SYSTEM
from libs.regex import js_css
from tools.textract.office import autocheck
from libs.logger import logger


def tikatext(filepath):
    return tikarser.from_file(filepath)["content"]


def plaintext(filepath, encoding='gbk'):
    try:
        with open(filepath, encoding=encoding) as fopen:
            return fopen.read()
    except UnicodeDecodeError:
        pass
    #
    other_charset = 'gbk' if encoding == 'utf-8' else 'utf-8'
    try:
        with open(filepath, encoding=other_charset) as fopen:
            return fopen.read()
    except UnicodeDecodeError:
        pass
    # gbk/utf-8均解码错误,使用tika解析
    if TIKA_SERVER_ACTIVE:
        return tikatext(filepath)
    return ''


def extract(filepath):
    content = ''
    if not os.path.exists(filepath):
        return content
    try:
        mime_class = mime_type = ''
        with open(filepath, 'rb') as fopen:
            # https://pypi.org/project/python-magic/
            mime_type = magic.from_buffer(fopen.read(2048), mime=True)
        if '/' in mime_type:
            mime_class = mime_type.split('/', 1)[0]
        # 1. 普通文本文件/HTML/JS/CSS文件直接读取解析
        if mime_class == 'text' or js_css.match(filepath):
            content = plaintext(filepath)
        # 2. 其他文档文件需使用特定工具解析
        else:
            # 优先使用tika解析
            if TIKA_SERVER_ACTIVE:
                content = tikatext(filepath)
            else:
                if re.match(r'.*\.(docx|xls[x]?|pptx|pdf)$', filepath, re.I):
                    content = autocheck(filepath)
                # linux不支持doc/ppt提取文本
                elif Platform == SYSTEM.WINDOWS and re.match(r'.*\.(doc|ppt)$', filepath, re.I):
                    content = autocheck(filepath)
    except:
        logger.error('提取文本失败: %s' % filepath)
        logger.error(traceback.format_exc())
    #
    content = content.strip()
    if content:
        logger.info('提取文本成功: %s' % filepath)
    return content


if __name__ == '__main__':
    from conf.paths import LOG_FILEPATH, CONF_PATH
    print(extract(CONF_PATH))
