#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from id_validator import validator


# 大陆居民身份证/港澳居民居住证/台湾居民居住证18位
# 不提取15位大陆居民身份证
idcard_pattern = re.compile(r'\b\d{17}(?:\d|X)\b', re.I)


def check_idcard(idcard):
    return validator.is_valid(idcard)


def find_idcard(text):
    text = str(text)
    # return [x for x in idcard_pattern.findall(text) if x]
    return [x for x in idcard_pattern.findall(text) if check_idcard(x)]


phone_pattern = re.compile(r'([\u4e00-\u9fa5 :：]{0,10}\s*)'
                           r'\b(13\d{9}|14[57]\d{8}|15\d{9}|166\d{8}|17[367]\d{8}|18\d{9})\b'
                           r'(\s*[\u4e00-\u9fa5]{0,10})')


def find_mobile(text):
    return phone_pattern.findall(text)


