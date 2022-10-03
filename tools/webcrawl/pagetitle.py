#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from urllib.parse import urlparse
from collections import namedtuple
from bs4 import BeautifulSoup
from utils.mixed import auto_decode
from libs.logger import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#
header = {
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}
#
RespInfo = namedtuple('RespInfo', ['url', 'title', 'html_text', 'status_code', 'desc'])


def req_get(url):
    parsed = urlparse(url)
    header['Referer'] = '%s://%s/' % (parsed.scheme, parsed.netloc)
    try:
        resp = requests.get(url, timeout=5, verify=False)
        html_text = auto_decode(resp.content)  # resp.text
        title = ''
        soup = BeautifulSoup(html_text, "html.parser")  # soup = BeautifulSoup(resp.text, "lxml")  标题乱码！Why?
        labels = soup.find_all('title')
        if len(labels) > 0:
            title = labels[0].text
        if resp.history:
            return req_get(resp.url)
        return RespInfo(url=url, title=title, html_text=html_text, status_code=resp.status_code, desc='')
    except Exception as e:
        logger.error('GET %s %s' % (url, e))
        return RespInfo(url=url, title='', html_text='', status_code=-1, desc=type(e).__name__)


if __name__ == '__main__':
    print(req_get('https://www.baidu.com'))

