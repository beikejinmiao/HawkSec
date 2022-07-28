#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import traceback
from tika import parser as tikarser
from conf.config import Platform, TIKA_SERVER_ACTIVE
from libs.enums import SYSTEM
from libs.regex import plain_text, html, js_css
from tools.textract.office import doc, docx, xls, xlsx, ppt, pptx, pdf
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
    # gbk/utf-8均解码错误，使用tika解析
    if TIKA_SERVER_ACTIVE:
        return tikatext(filepath)
    return ''


__office_methods = {
    'doc': doc,
    'docx': docx,
    'xls': xls,
    'xlsx': xlsx,
    'ppt': ppt,
    'pptx': pptx,
    'pdf': pdf,
}


def windows(filepath):
    suffix = os.path.basename(filepath).split('.')[-1].lower()
    content = ''
    # 普通文本文件、HTML、JS、CSS文件直接读取解析
    if plain_text.match(filepath) or html.match(filepath) or js_css.match(filepath):
        content = plaintext(filepath)
    elif re.match(r'.*\.(doc[x]?|xls[x]?|ppt[x]?|pdf)$', filepath, re.I):
        content = __office_methods[suffix](filepath)
    logger.info('提取文本成功: %s' % filepath)
    return content


def linux(filepath):
    content = plaintext(filepath)
    logger.info('提取文本成功: %s' % filepath)
    return content


def extract(filepath):
    content = ''
    try:
        if Platform == SYSTEM.WINDOWS:
            content = windows(filepath)
        elif Platform == SYSTEM.LINUX:
            content = linux(filepath)
        else:
            logger.warning('Not supported system: %s' % Platform)
    except:
        logger.error('提取文本失败: %s' % filepath)
        logger.error(traceback.format_exc())
    return content
