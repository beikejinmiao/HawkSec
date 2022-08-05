#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from urllib.parse import urlparse


def abspath(url, site=None):
    """
    获取绝对路径URL
    将相对路径URL转成绝对路径URL,避免同一URL被重复爬取
    """
    if not site:
        site = urlparse(url).netloc
    if "#" in url:
        # 移除页面内部定位符井号#,其实是同一个链接
        url = url[0:url.rfind('#')]
    while '/./' in url:
        url = url.replace('/./', '/')
    ix = url.index(site) + len(site)
    host, url_path = url[:ix], url[ix:]
    while '/../' in url_path:
        url_path = re.sub(r'(^|/[^/]+)/\.\./', '/', url_path)
    return '{host}{connector}{path}'.format(host=host,
                                            connector='' if url_path.startswith('/') else '/',
                                            path=url_path)


if __name__ == '__main__':
    urls = [
        'https://cms.baidu.com/../1/./2/3/4/../../../docs/2022-07/f9593.png',
        'https://cms.baidu.com/../../1/./2/3/4/../../../docs/2022-07/f9593.png',
        'https://cms.baidu.com/../1/./2/3/4/../.5./../docs/2022-07/f9593.png',
        'https://cms.baidu.com/../../../docs/2022-07/f9593.png',
        'https://cms.baidu.com../../../docs/2022-07/f9593.png',
        'https://cms.baidu.com/../1/./2//,/3/4/../../../docs/2022-07/f9593.png',
    ]
    for u in urls:
        print(abspath(u))
