#!/usr/bin/env python
# -*- coding:utf-8 -*-
import enum

QMSG_BOX_REPLY_YES = 1
QMSG_BOX_REPLY_NO = 0


SENSITIVE_FLAG_URL = 0
SENSITIVE_FLAG_IDCARD = 1
SENSITIVE_FLAG_MOBILE = 2
SENSITIVE_FLAG_KEYWORD = 3


# AttributeError: module 'enum' has no attribute 'IntFlag'
class SENSITIVE_FLAG(enum.IntEnum):
    URL = U = SENSITIVE_FLAG_URL
    IDCARD = I = SENSITIVE_FLAG_IDCARD
    MOBILE = M = SENSITIVE_FLAG_MOBILE
    KEYWORD = K = SENSITIVE_FLAG_KEYWORD


class SENSITIVE_NAME(enum.Enum):
    URL = "外链"
    IDCARD = "身份证"
    MOBILE = "手机号码"
    KEYWORD = "关键字"


sensitive_flag_name = {
    SENSITIVE_FLAG.URL: SENSITIVE_NAME.URL,
    SENSITIVE_FLAG.IDCARD: SENSITIVE_NAME.IDCARD,
    SENSITIVE_FLAG.MOBILE: SENSITIVE_NAME.MOBILE,
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


class TABLES_CN(enum.Enum):
    CrawlStat = "Url&File爬取状态统计"
    Extractor = "Url&File敏感内容统计"
    FileType = "压缩文件类型"
    WhiteList = "Url&File白名单"
    Sensitives = "敏感内容来源统计"


tables_cn_name = {
    TABLES.CrawlStat.value: TABLES_CN.CrawlStat.value,
    TABLES.Extractor.value: TABLES_CN.Extractor.value,
    TABLES.FileType.value: TABLES_CN.FileType.value,
    TABLES.WhiteList.value: TABLES_CN.WhiteList.value,
    TABLES.Sensitives.value: TABLES_CN.Sensitives.value,
}

if __name__ == '__main__':
    # print(SYSTEM('Windows') is SYSTEM.WINDOWS)
    print('windows' == SYSTEM.WINDOWS)

