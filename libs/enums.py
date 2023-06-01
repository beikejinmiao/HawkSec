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
class SensitiveFlag(enum.IntEnum):
    URL = U = SENSITIVE_FLAG_URL
    IDCARD = I = SENSITIVE_FLAG_IDCARD
    MOBILE = M = SENSITIVE_FLAG_MOBILE
    KEYWORD = K = SENSITIVE_FLAG_KEYWORD


class SensitiveName(enum.Enum):
    URL = "外链"
    IDCARD = "身份证"
    MOBILE = "手机号码"
    KEYWORD = "关键字"


sensitive_flag_name = {
    SensitiveFlag.URL: SensitiveName.URL,
    SensitiveFlag.IDCARD: SensitiveName.IDCARD,
    SensitiveFlag.MOBILE: SensitiveName.MOBILE,
    SensitiveFlag.KEYWORD: SensitiveName.KEYWORD,
}


class System(str, enum.Enum):
    # https://stackoverflow.com/questions/58608361/string-based-enum-in-python
    LINUX = "linux"
    WINDOWS = "windows"
    DARWIN = "darwin"


class Tables(enum.Enum):
    CrawlStat = "crawlstat"
    Extractor = "extractor"
    FileType = "filetype"
    WhiteList = "whitelist"
    Sensitives = "sensitives"


class TablesCn(enum.Enum):
    CrawlStat = "Url&File爬取状态统计"
    Extractor = "Url&File敏感内容统计"
    FileType = "压缩文件类型"
    WhiteList = "Url&File白名单"
    Sensitives = "敏感内容来源统计"


tables_cn_name = {
    Tables.CrawlStat.value: TablesCn.CrawlStat.value,
    Tables.Extractor.value: TablesCn.Extractor.value,
    Tables.FileType.value: TablesCn.FileType.value,
    Tables.WhiteList.value: TablesCn.WhiteList.value,
    Tables.Sensitives.value: TablesCn.Sensitives.value,
}

if __name__ == '__main__':
    # print(SYSTEM('Windows') is SYSTEM.WINDOWS)
    print('windows' == System.WINDOWS)

