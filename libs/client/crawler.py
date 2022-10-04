#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from urllib.parse import urlparse
from collections import deque, namedtuple
from collections.abc import Iterable
from bs4 import BeautifulSoup
from conf.config import http_headers
from libs.regex import img, video, executable
from utils.mixed import auto_decode
from libs.web.url import urlsite, normal_url
from libs.web.url import urlfile, absurl
from libs.logger import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Spider(object):
    def __init__(self, start_url, same_site=True, headers=None, timeout=10, hsts=False):
        self._start_url = normal_url(start_url)
        self.site = urlsite(self._start_url).reg_domain
        # 是否限制只爬取同站网页
        if same_site is False or same_site is None:
            self._site_allows = None           # 不做任何限制
        else:
            self._site_allows = set()
            self._site_allows.add(self.site)   # 默认包含本站
            if isinstance(same_site, Iterable):
                for site in same_site:
                    self._site_allows.add(urlsite(site).reg_domain)    # 限定范围
        #
        self.urls = dict()          # key: url, value: 该url的来源地址
        self.urls[start_url] = start_url
        self._broken_urls = dict()
        self._file_urls = dict()
        self.__urlpath_limit = dict()       # 限制某个URL路径下的最大数量(某些查询页面参数组合范围极大)
        self.__parsed_urls = set()
        #
        self.session = requests.session()
        self.session.headers = headers if isinstance(headers, dict) and len(headers) > 0 else http_headers
        self.timeout = timeout
        #
        self.hsts = hsts                    # 是否只访问HTTPS网站链接

    RespInfo = namedtuple('RespInfo', ['status_code', 'url', 'filename', 'html_text', 'desc'])

    def scrape(self, path_limit=None):
        """
        执行爬取&提取页面url操作
        """
        status_code = 0
        new_urls = deque([self._start_url])
        while len(new_urls):
            url = new_urls.popleft()
            # 提取url site和url路径
            """
            urlparse('https://xsc.baidu.cn/node/docs/49716.htm')
            >> ParseResult(scheme='https', netloc='xsc.baidu.cn', path='/node/docs/49716.htm', params='', query='', fragment='')
            urlparse('https://xsc.baidu.cn/?q=node/49716.htm')
            >> ParseResult(scheme='https', netloc='xsc.baidu.cn', path='/', params='', query='q=node/49716.htm', fragment='')
            urlparse('https://xsc.baidu.cn')    # 注意
            >> ParseResult(scheme='https', netloc='xsc.baidu.cn', path='', params='', query='', fragment='')
            """
            parts = urlparse(url)
            site = "{0.scheme}://{0.netloc}".format(parts)
            # 针对某些查询页面,参数组合范围极大,需要限制该路径下的URL数量,避免任务无法结束
            urlpath = site + parts.path
            if urlpath not in self.__urlpath_limit:
                self.__urlpath_limit[urlpath] = 1
            else:
                _path_cnt_ = self.__urlpath_limit[urlpath]
                if _path_cnt_ > 5000:
                    continue
                self.__urlpath_limit[urlpath] = _path_cnt_ + 1
            # 处理文件链接(文件过大下载较慢,影响爬取速度)
            filename = urlfile(url)
            if self.filter(filename):
                continue
            if filename:
                self._file_urls[url] = self.urls.get(url)
                yield self.RespInfo(status_code=status_code, url=url, filename=filename, html_text=None, desc='')
                continue
            # 爬取正常网页
            try:
                resp = self.session.get(url, timeout=self.timeout, verify=False)
                status_code = resp.status_code
                logger.info('GET %s %s' % (url, status_code))
                # https://stackoverflow.com/questions/20475552/python-requests-library-redirect-new-url
                # 如果发生重定向,更新URL,避免提取页面href后拼接错误新URL(大量404)
                if resp.history:
                    logger.info('!RedirectTo: %s' % resp.url)
                    self.urls[url] = '302'
                    self.urls[resp.url] = url
                    url = absurl(resp.url, site=self.site)  # 更新重定向后的URL
                    # 再次处理文件链接
                    filename = urlfile(url)
                    if filename:
                        self._file_urls[url] = self.urls.get(url)
                        yield self.RespInfo(status_code=status_code, url=url, filename=filename, html_text=None, desc='')
                        continue
            # except (MissingSchema, InvalidURL, InvalidSchema, ConnectionError, ReadTimeout) as e:
            except Exception as e:
                logger.error('GET %s %s' % (url, e))
                self._broken_urls[url] = self.urls.get(url, '')
                yield self.RespInfo(status_code=-1, url=url, filename=None, html_text=None, desc=type(e).__name__)
                continue
            # 针对已解析过的URL页面,忽略 -- 某些重定向页面(404/403等被重定向至固定页面)会反复出现
            if url in self.__parsed_urls:
                continue
            self.__parsed_urls.add(url)
            # 获取当前链接的目录路径,用于本站内部相对路径href拼接
            urldir = url[:url.rfind('/') + 1] if '/' in parts.path else url
            urldir = urldir if urldir.endswith('/') else (urldir + '/')  # 和href拼接时需要有/
            # 解析HTML页面
            html_text = auto_decode(resp.content)       # resp.text
            soup = BeautifulSoup(resp.text, "lxml")  # soup = BeautifulSoup(html_text, "html.parser")
            yield self.RespInfo(status_code=status_code, url=url, filename=None, html_text=html_text, desc=resp.reason)
            # 提取页面内容里的URL
            links = soup.find_all('a')
            for link in links:
                new_url = ''
                # 从<a>标签中提取href
                href = link.attrs["href"] if "href" in link.attrs else ''
                if href.startswith("#") or href.startswith('javascript:'):
                    continue
                if href.startswith("http://") or href.startswith("https://"):
                    new_url = href
                elif href.startswith("/"):
                    # 绝对路径href
                    new_url = site + href
                else:
                    # 相对路径href
                    new_url = urldir + href
                if self._site_allows is not None and urlsite(new_url).reg_domain not in self._site_allows:
                    continue
                new_url = absurl(new_url, site=self.site)
                # 限制URL
                if path_limit and path_limit not in new_url:
                    continue
                if self.hsts and new_url.startswith('http://'):
                    new_url = 'https://' + new_url[7:]
                new_url = normal_url(new_url)
                if new_url and new_url not in self.urls:
                    self.urls[new_url] = url  # 保存该new_url的来源地址
                    new_urls.append(new_url)

    def filter(self, path):
        # 默认忽略图片、音频、视频、可执行文件
        if img.match(path) or video.match(path) or executable.match(path):
            return True
        return False


if __name__ == '__main__':
    spider = Spider('https://rtx.bcsa.edu.cn/lixiao.html')
    from libs.regex import find_urls
    for resp in spider.scrape():
        if resp.html_text:
            print(find_urls(resp.html_text))

