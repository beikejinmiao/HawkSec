#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from bs4 import BeautifulSoup

"""
从网页中提取所有链接和标题

https://stackoverflow.com/questions/2725156/complete-list-of-html-tag-attributes-which-have-a-url-value
https://www.w3.org/TR/REC-html40/index/attributes.html
"""

URL_LABELS = {
    'a': 'href',
    'area': 'href',
    'base': 'href',
    'link': 'href',

    'script': 'src',
    'audio': 'src',
    'embed': 'src',
    'source': 'src',
    'track': 'src',

    'frame': ('src', 'longdesc'),
    'iframe': ('src', 'longdesc'),
    'img': ('src', 'longdesc', 'usemap', 'lowsrc', 'dynsrc'),
    'video': ('src', 'poster'),
    'input': ('src', 'usemap', 'formaction'),

    'q': 'cite',
    'del': 'cite',
    'ins': 'cite',
    'blockquote': 'cite',

    'form': 'action',
    'head': 'profile',
    'applet': 'codebase',
    'body': 'background',
    'button': 'formaction',
    'command': 'icon',
    'meta': 'content',
    'html': ('xmlns', 'manifest'),
    'object': ('classid', 'codebase', 'data', 'usemap'),
}


def _is_url(text):
    return True if re.match(r'[A-Za-z]+://.+', text) else False


A_HREF_REGEX = re.compile(r'<a.+href=[\'"](\w+://.+?)[\'"].*>(.+?)</a>')


def a(text, regex=False):
    if not regex:
        urls_title = dict()  # key: url, value: title
        soup = BeautifulSoup(text, "lxml")
        for ele in soup.find_all('a'):
            if 'href' in ele.attrs and _is_url(ele.attrs['href']):
                urls_title[ele.attrs['href']] = ele.string
    else:
        urls_title = dict(A_HREF_REGEX.findall(text))
    return urls_title


def urlfind(text):
    urls_title = dict()               # key: url, value: title
    #
    soup = BeautifulSoup(text, "lxml")
    for label, attr in URL_LABELS.items():
        for ele in soup.find_all(label):
            if isinstance(attr, (tuple, list)):
                for _attr_ in attr:
                    if _attr_ in ele.attrs and _is_url(ele.attrs[_attr_]):
                        urls_title[ele.attrs[_attr_]] = ele.string
            elif attr in ele.attrs and _is_url(ele.attrs[attr]):
                urls_title[ele.attrs[attr]] = ele.string
    #
    candidates = re.findall(r'url\(([A-Za-z]+://.+)\)', text)       # <div style="background: url(image.png)">
    if len(candidates) > 0:
        urls_title[candidates[0]] = None
    return urls_title


test_html = """
<!DOCTYPE html>
<html xmlns:wb="http://open.weibo.com/wb" lang="zh">
<body>
<head>
    <meta name="TileImage" content="http://p2.ifengimg.com/8cbe73a7378dafdb/2013/0416/logo.png">
    <script src="https://x0.ifengimg.com/fe/shank/content/2019/0418/fa.min.js" type="text/javascript"></script>
</head>
    <iframe src="https://www.w3schools.com"></iframe>
    <div style="background: url(https://www.w3schools.com/images/w3lynx_200.png)">
    <a href="https://www.google.com/search?q=lowsrc+dynsrc&newwindow=1&hl=zh-CN&sxsrf=-qQiuofrg%3A16&sclient=gws-wiz">凤凰纲</a>
    <!--<a href="http://www.jingduzhisheng.com/">京都之声</a>
    <a href="http://stu.chinacampus.org/">中国大学生年度人物评选</a>-->
    <div class="lefti">
        <a href="https://weibo.com/p/1002065293024672/home?is_all=1"><img src="./images/0508wb.png" />关注官方微博</a>
    </div>
</body>
</html>
"""


if __name__ == '__main__':
    print(a(test_html, regex=True))
