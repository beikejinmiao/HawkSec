#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.mixed import urlsite

data = [
    'https://123/asds', 'sftp://www.baidu.com/asds', 'qwe://www.baidu.com/asds', 'https://1.1.1.1/asds'
    '1.1.1.1/asds', 'www.baidu.com/asds', 'host/asds'
]

for item in data:
    print(item)
    print('>>', urlsite(item, tld=True))
