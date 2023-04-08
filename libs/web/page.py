#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import traceback
import requests
from requests import HTTPError
from urllib.parse import urlparse
from http.client import responses
from bs4 import BeautifulSoup
from conf.config import http_headers
from libs.regex import html
from libs.web.pywget import auto_decode, detect_filename
from libs.web.url import urlfile, normal_url
from libs.logger import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RespInfo(object):
    def __init__(self, url='', title=None, text='', status_code=-1, desc=''):
        self.url = url.strip()
        self.title = title
        self.text = text
        self.status_code = status_code
        self.desc = desc if desc else responses.get(status_code, '')

    def __str__(self):
        d = self.__dict__.copy()
        del d['text']
        return str(d)


def try_crawl(url, resp=None, max_depth=4):
    """
    :param url:
    :param resp: 重定向追踪中的前一次响应内容
    :param max_depth: 设置重定向追踪爬取最大深度,避免RecursionError
    :return:
    """
    try:
        parsed = urlparse(url)
        http_headers['Referer'] = '%s://%s/' % (parsed.scheme, parsed.netloc)
        resp = requests.get(normal_url(url), timeout=5, headers=http_headers, verify=False)
        resp.raise_for_status()
        if resp.history and max_depth > 0:
            return try_crawl(resp.url, resp=resp, max_depth=max_depth-1)
    except HTTPError:
        return RespInfo(url=url, status_code=resp.status_code, desc=resp.reason)
    except Exception as e:
        logger.error('crawl url error: %s %s' % (url, repr(e)))
        # logger.error(traceback.format_exc())
        return RespInfo(url=url, status_code=-1, desc=type(e).__name__)
    #
    text = auto_decode(resp.content, default=resp.text)
    # 如果发生重定向,那么url内容是重定向后的url
    return RespInfo(url=url, text=text, status_code=resp.status_code, desc=resp.reason)


"""
提取页面标题
"""


def strip(text):
    return re.sub(r'[\r\n\t]+', '', text).strip() if text else ''


def __page_info(url):
    title = ''
    # 只爬取html网页内容
    resp_info = try_crawl(url)
    try:
        if resp_info.text:
            soup = BeautifulSoup(resp_info.text, "lxml")  # soup = BeautifulSoup(resp.text, "lxml")
            title_labels = soup.find_all('title')
            if title_labels:
                title = title_labels[0].text
            resp_info.title = strip(title)
    except TypeError:
        # BeautifulSoup解析图片时：  TypeError: object of type 'NoneType' has no len()
        pass
    except:
        logger.error('find title error: %s' % url)
        logger.error(traceback.format_exc())
    # title为空时,默认使用从url中提取文件名
    if not resp_info.title:
        resp_info.title = urlfile(url)
    #
    if not resp_info.desc:
        resp_info.desc = responses.get(resp_info.status_code, '')
    return resp_info


def page_info(url):
    if html.match(url) or url.endswith('/'):
        return __page_info(url)
    #
    head_resp = requests.head(url, timeout=2, verify=False)
    content_type = ''
    for header in head_resp.headers:
        if header.lower() == 'content-type':
            content_type = head_resp.headers[header].split(';')[0].strip()
            break
    if content_type.startswith('text/'):
        return __page_info(url)
    return RespInfo(url=url,
                    title=detect_filename(url, None, head_resp.headers),
                    status_code=head_resp.status_code)


def page_title(url):
    return page_info(url).title


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


def page_a_href(text, regex=False):
    if not regex:
        _urls_title = dict()  # key: url, value: title
        soup = BeautifulSoup(text, "lxml")
        for ele in soup.find_all('a'):
            if 'href' in ele.attrs and _is_url(ele.attrs['href']):
                _urls_title[ele.attrs['href']] = strip(ele.string)
    else:
        _urls_title = dict(A_HREF_REGEX.findall(text))
    #
    urls_title = dict()
    for url, title in _urls_title.items():
        title = title.strip('\r\n ') if title else ''
        urls_title[normal_url(url)] = title[:min(128, len(title))]
    return urls_title


def page_href(text):
    _urls_title = dict()               # key: url, value: title
    #
    soup = BeautifulSoup(text, "lxml")
    for label, attr in URL_LABELS.items():
        for ele in soup.find_all(label):
            if isinstance(attr, (tuple, list)):
                for _attr_ in attr:
                    if _attr_ in ele.attrs and _is_url(ele.attrs[_attr_]):
                        _urls_title[ele.attrs[_attr_]] = strip(ele.string)
            elif attr in ele.attrs and _is_url(ele.attrs[attr]):
                _urls_title[ele.attrs[attr]] = strip(ele.string)
    #
    candidates = re.findall(r'url\(([A-Za-z]+://.+)\)', text)       # <div style="background: url(image.png)">
    if len(candidates) > 0:
        _urls_title[candidates[0]] = ''
    #
    urls_title = dict()
    for url, title in _urls_title.items():
        urls_title[normal_url(url)] = title.strip('\r\n ') if title else ''
    return urls_title


if __name__ == '__main__':
    print(page_title('https://www.bwu.edu.cn'))

