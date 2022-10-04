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
from utils.mixed import auto_decode
from libs.web.url import urlfile, normal_url
from libs.logger import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RespInfo(object):
    def __init__(self, url='', title='', html_text='', status_code=-1, desc='', response=None):
        self.url = url.strip()
        self.title = title
        self.html_text = html_text
        self.status_code = status_code
        self.desc = desc
        self.response = response

    def __str__(self):
        return str({'url': self.url, 'title': self.title, 'status_code': self.status_code, 'desc': self.desc})


def try_crawl(url, resp=None):
    parsed = urlparse(url)
    http_headers['Referer'] = '%s://%s/' % (parsed.scheme, parsed.netloc)
    try:
        resp = requests.get(url, timeout=5, headers=http_headers, verify=False)
        resp.raise_for_status()
        if resp.history:
            return try_crawl(resp.url, resp=resp)
    except HTTPError:
        return RespInfo(url=url, status_code=resp.status_code, desc=resp.reason, response=resp)
    return RespInfo(url=url, html_text=auto_decode(resp.content),
                    status_code=resp.status_code, desc=resp.reason, response=resp)


"""
提取页面标题
"""


def pagetitle(url):
    title = ''
    resp_info = None
    try:
        resp_info = try_crawl(url)
        soup = BeautifulSoup(resp_info.html_text, "html.parser")  # soup = BeautifulSoup(resp.text, "lxml")  标题乱码！Why?
        title_label = soup.find_all('title')
        if len(title_label) > 0:
            title = title_label[0].text
        resp_info.title = title
    except Exception as e:
        if resp_info is None:
            resp_info = RespInfo(url=url, status_code=-1, desc=type(e).__name__)
        logger.debug(traceback.format_exc())
        logger.error('find title error: %s %s' % (url, e))
    # title为空时,尝试从url中提取文件名
    if not resp_info.title:
        resp_info.title = urlfile(url)
    #
    if not resp_info.desc:
        resp_info.desc = responses.get(resp_info.status_code, '')
    return resp_info


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


def find_a_href(text, regex=False):
    if not regex:
        _urls_title = dict()  # key: url, value: title
        soup = BeautifulSoup(text, "lxml")
        for ele in soup.find_all('a'):
            if 'href' in ele.attrs and _is_url(ele.attrs['href']):
                _urls_title[ele.attrs['href']] = ele.string
    else:
        _urls_title = dict(A_HREF_REGEX.findall(text))
    #
    urls_title = dict()
    for url, title in _urls_title.items():
        urls_title[normal_url(url)] = title.strip('\r\n ') if title else ''
    return urls_title


def find_url(text):
    _urls_title = dict()               # key: url, value: title
    #
    soup = BeautifulSoup(text, "lxml")
    for label, attr in URL_LABELS.items():
        for ele in soup.find_all(label):
            if isinstance(attr, (tuple, list)):
                for _attr_ in attr:
                    if _attr_ in ele.attrs and _is_url(ele.attrs[_attr_]):
                        _urls_title[ele.attrs[_attr_]] = ele.string
            elif attr in ele.attrs and _is_url(ele.attrs[attr]):
                _urls_title[ele.attrs[attr]] = ele.string
    #
    candidates = re.findall(r'url\(([A-Za-z]+://.+)\)', text)       # <div style="background: url(image.png)">
    if len(candidates) > 0:
        _urls_title[candidates[0]] = ''
    #
    urls_title = dict()
    for url, title in _urls_title.items():
        urls_title[normal_url(url)] = title.strip('\r\n ') if title else ''
    return urls_title

