#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import pandas as pd
from id_validator import validator
from bs4 import BeautifulSoup


# 大陆居民身份证/港澳居民居住证/台湾居民居住证18位
# 不提取15位大陆居民身份证
idcard_pattern = re.compile(r'\b\d{17}(?:\d|X)\b', re.I)


def check_idcard(idcard):
    return validator.is_valid(idcard)


def find_idcard(text):
    text = str(text)
    # return [x for x in idcard_pattern.findall(text) if x]
    return [x for x in idcard_pattern.findall(text) if check_idcard(x)]


phone_pattern = re.compile(r'\b(13\d{9}|14[57]\d{8}|15\d{9}|166\d{8}|17[367]\d{8}|18\d{9})\b')


def find_mobile(text):
    phone_names = list()
    if phone_pattern.search(text):
        soup = BeautifulSoup(text, "lxml")
        # 处理表格
        # tables = soup.find_all('table')
        # for table in tables:
        #     html_table(str(table))
        # soup.table.decompose()
        #
        results = soup.find_all(text=phone_pattern)
        for item in results:
            # item = re.sub(r'\s*[（(].*[)）]\s*', '', item)          # 括号之中可能是姓名或者手机号码
            # https://blog.csdn.net/chivalrousli/article/details/77412329
            #   中文字符的Unicode范围： [\u4e00-\u9fa5]
            #   全角ASCII、全角中英文标点、半宽片假名、半宽平假名、半宽韩文字母范围：[\uff00-\uffef]
            # item = re.sub(r'[^\x00-\x7E\u2e80-\ufe4f\uff00-\uffef]+', '', item)
            item = re.sub(r'[^\x00-\x7E\u4e00-\u9fa5\uff00-\uffef]+', ' ', item)    # 移除非ASCII、非中文、非全角符号
            item = re.sub(r'[\x00-\x20]+', ' ', item)                               # 将ASCII控制字符替换为空格
            item = re.sub(r'^[\s:;,).：；，）。]+', '', item)                         # 替换行首无关字符
            if item.endswith(';') or item.endswith('；'):
                item = item[:-1]
            phone_names.append(item)
    return phone_names

#
# def html_table(table_html):
#     df = pd.read_html(table_html)[0].fillna('')
#     print(df)
#
