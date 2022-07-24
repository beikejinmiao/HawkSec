#!/usr/bin/env python
# -*- coding:utf-8 -*-
import enum

SENSITIVE_FLAG_URL = 0
SENSITIVE_FLAG_IDCARD = 1
SENSITIVE_FLAG_KEYWORD = 2


class SENSITIVE_FLAG(enum.IntFlag):
    URL = U = SENSITIVE_FLAG_URL
    IDCARD = I = SENSITIVE_FLAG_IDCARD
    KEYWORD = K = SENSITIVE_FLAG_KEYWORD


class SENSITIVE_NAME(enum.Enum):
    URL = "外链"
    IDCARD = "身份证"
    KEYWORD = "关键字"


sensitive_flag_name = {
    SENSITIVE_FLAG.URL: SENSITIVE_NAME.URL,
    SENSITIVE_FLAG.IDCARD: SENSITIVE_NAME.IDCARD,
    SENSITIVE_FLAG.KEYWORD: SENSITIVE_NAME.KEYWORD,
}


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
    Sensitives = "sensitives"


if __name__ == '__main__':
    # print(SYSTEM('Windows') is SYSTEM.WINDOWS)
    print('windows' == SYSTEM.WINDOWS)

