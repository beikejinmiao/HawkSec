#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import traceback
from conf.config import PLATFORM
from libs.enums import SYSTEM
from libs.regex import plain_text, html, js_css
from libs.logger import logger
from tools.textract.office import doc, docx, xls, xlsx, ppt, pptx, pdf
from tools.textract.tika import tikatext


office_extract = {
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
        try:
            with open(filepath, encoding='gbk') as fopen:
                content = fopen.read()
        except UnicodeDecodeError:
            with open(filepath, encoding='utf-8') as fopen:
                content = fopen.read()
        # # gbk/utf-8均解码错误，使用tika解析
        # except:
        #     content = parser.from_file(filepath)["content"]
    elif re.match(r'.*\.(doc[x]?|xls[x]?|ppt[x]?|pdf)$', filepath, re.I):
        content = office_extract[suffix](filepath)
    #
    logger.error('Extract text success: %s' % filepath)
    return content


def linux(filepath):
    content = tikatext(filepath)
    logger.error('Extract text success: %s' % filepath)
    return content


def extract(filepath):
    content = ''
    try:
        if PLATFORM == SYSTEM.WINDOWS:
            content = windows(filepath)
        elif PLATFORM == SYSTEM.LINUX:
            content = linux(filepath)
        else:
            logger.warning()
    except:
        logger.error('Extract text error: %s' % filepath)
        logger.error(traceback.format_exc())
    return content
