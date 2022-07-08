#!/usr/bin/env python
# -*- coding:utf-8 -*-
import enum


class SensitiveFLAG(enum.IntFlag):
    URL = U = 1
    IDCARD = I = 2
    KEYWORD = K = 4


class SYSTEM(str, enum.Enum):
    # https://stackoverflow.com/questions/58608361/string-based-enum-in-python
    LINUX = "linux"
    WINDOWS = "windows"
    DARWIN = "darwin"


if __name__ == '__main__':
    # print(SYSTEM('Windows') is SYSTEM.WINDOWS)
    print('windows' == SYSTEM.WINDOWS)

