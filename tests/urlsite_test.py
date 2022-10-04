#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tools import htmlurl
from libs.web import pagetitle
from libs.web import urlsite

data = [
    'https://123/asds', 'sftp://www.baidu.com/asds', 'qwe://www.baidu.com/asds', 'https://1.1.1.1/asds'
    '1.1.1.1/asds', 'www.baidu.com/asds', 'host/asds'
]

for item in data:
    print(item)
    print('>>', urlsite(item))


url = 'https://www.bch.com.cn'
# resp = requests.get(url, headers=headers)
text = """
 <a href="https://www.stjude.org/ " target="_blank">美国圣裘德儿童研究医院</a></p>
 </li>
 <li><a href="https://chicagomedicalcenter.com/ " >
 </a>
 <p>
 <a href="https://chicagomedicalcenter.com/ " target="_blank">美国芝加哥大学医学中心</a></p>
 </li>
 <li><a href="http://www.ucla.edu/ " >
 </a>
 <p>
 <a href="http://www.ucla.edu/ " target="_blank">美国加州大学洛杉矶分校</a></p>
 </li>
 <li><a href="http://www.ufl.edu/ " >
 </a>
 <p>
"""
print(htmlurl.a(text))
print(pagetitle('https://chicagomedicalcenter.com/'))

