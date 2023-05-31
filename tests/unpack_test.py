#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.filedir import traverse
from tools.unzip import unpack

paths = traverse(r'D:\PycharmProjects\HawkSec\zdump\downloads\Python-3.8.10.tgz.unpack\Python-3.8.10')
print(len(paths))

# 卡死
unpack(r'D:\PycharmProjects\HawkSec\zdump\downloads\Python-3.8.10.tgz')
