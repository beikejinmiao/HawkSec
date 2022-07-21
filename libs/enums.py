#!/usr/bin/env python
# -*- coding:utf-8 -*-
import enum

SENSITIVE_FLAG_URL = 0
SENSITIVE_FLAG_IDCARD = 1
SENSITIVE_FLAG_KEYWORD = 2


class SensitiveType(enum.IntFlag):
    URL = U = SENSITIVE_FLAG_URL
    IDCARD = I = SENSITIVE_FLAG_IDCARD
    KEYWORD = K = SENSITIVE_FLAG_KEYWORD


class SYSTEM(str, enum.Enum):
    # https://stackoverflow.com/questions/58608361/string-based-enum-in-python
    LINUX = "linux"
    WINDOWS = "windows"
    DARWIN = "darwin"


class TABLES(enum.Enum):
    CrawlStat = "crawlstat"
    Extractor = "extractor"
    FileType = "filetype"
    WhiteList = "whitelist"


if __name__ == '__main__':
    # print(SYSTEM('Windows') is SYSTEM.WINDOWS)
    print('windows' == SYSTEM.WINDOWS)

