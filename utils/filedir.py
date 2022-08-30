#!/usr/bin/env python
# -*- coding:utf-8 -*-
import io
import os
import json
from conf.paths import PRIVATE_RESOURCE_HOME
from libs.logger import logger


def writer(path, texts, method="w", encoding='utf-8'):
    with open(path, method, encoding=encoding) as fout:
        if isinstance(texts, str):
            fout.write(texts)
        elif isinstance(texts, dict):
            json.dump(texts, fout, indent=4)
        else:
            fout.write('\n'.join(texts))


def _reader_(path, encoding, skip_blank=True):
    with io.open(path, encoding=encoding) as fopen:
        while True:
            try:
                line = fopen.readline()
            except Exception as e:
                # UnicodeDecodeError: 'utf8' codec can't decode byte 0xfb in position 17: invalid start byte
                raise e
            if not line:
                break
            # check the line whether is blank or not
            line = line.strip()
            if skip_blank and not line:
                continue
            yield line


def reader(path, encoding='utf-8', skip_blank=True, raisexp=False):
    charsets = ['gbk', 'utf-8']
    if encoding not in charsets:
        charsets.append(encoding)
    # 尝试多种编码方式
    failed_charsets = set()
    for charset in charsets:
        try:
            for line in _reader_(path, charset, skip_blank=skip_blank):
                yield line
        except UnicodeDecodeError as e:
            failed_charsets.add(charset)
            continue
        except Exception as e:
            if raisexp:
                raise e
        break
    if len(failed_charsets) == len(charsets):
        logger.error("编码错误导致读取文件失败，目前只支持GBK和UFT-8编码: '%s'" % path)
    else:
        logger.info("读取文件成功成功: '%s'" % path)


def traverse(top, contains=None):
    files = list()
    if not top:
        return files
    if not os.path.exists(top):
        logger.warning("'%s' is not existed" % top)
        return files
    if os.path.isfile(top):
        files.append(top)
        return files

    for root, dirs, filenames in os.walk(top):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if contains and contains not in filename:
                continue
            files.append(file_path)
    return files


class StyleSheetHelper(object):
    @staticmethod
    def __load_qss(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def load_qss(name):
        qss_path = os.path.join(PRIVATE_RESOURCE_HOME, 'css', '%s.qss' % name)
        return StyleSheetHelper.__load_qss(qss_path)



