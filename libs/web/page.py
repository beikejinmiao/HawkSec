#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
import requests
from requests import HTTPError
from urllib.parse import urlparse
from http.client import responses
from bs4 import BeautifulSoup
from conf.config import http_headers
from utils.mixed import auto_decode
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
    if not resp_info.desc:
        resp_info.desc = responses.get(resp_info.status_code, '')
    return resp_info


if __name__ == '__main__':
    print(pagetitle('https://www.baidu.com/'))

