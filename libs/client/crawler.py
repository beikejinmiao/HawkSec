#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import requests
from urllib.parse import urlparse
from collections import deque, namedtuple
from bs4 import BeautifulSoup
from libs.regex import html, common_dom
from libs.regex import img, video, executable
from utils.mixed import auto_decode, urlsite
from libs.logger import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

default_headers = {
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
}


def url_file(url):
    if url.endswith('/'):
        return ''
    url = urlparse(url).path    # 移除URL参数
    if html.match(url) or common_dom.match(url):
        return ''
    if re.match(r'.+\.\w{2,5}$', url) and not re.match(r'.+\.[\d_]+$', url):
        return os.path.basename(url)
    return ''


class Spider(object):
    def __init__(self, start_url, same_site=True, headers=None, timeout=10, hsts=False):
        self._start_url = start_url
        self.site = urlsite(start_url).reg_domain
        self.same_site = same_site          # 是否限制只爬取同站网页
        #
        self.all_urls = dict()          # key: url, value: 该url的来源地址
        self.all_urls[start_url] = start_url
        self.broken_urls = dict()
        self.file_urls = dict()
        self.__urlpath_limit = dict()       # 限制某个URL路径下的最大数量(某些查询页面参数组合范围极大)
        self.__parsed_urls = set()
        #
        self.session = requests.session()
        self.session.headers = headers if isinstance(headers, dict) and len(headers) > 0 else default_headers
        self.timeout = timeout
        #
        self.hsts = hsts                    # 是否只访问HTTPS网站链接

    @staticmethod
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
        # path需以斜杠/开始,要不会陷入死循环
        # https://cms.baidu.com../../images/2022-07/f9593.png
        if not url_path.startswith('/'):
            url_path = '/' + url_path
        while '/../' in url_path:
            url_path = re.sub(r'(^|/[^/]+)/\.\./', '/', url_path)
        url_path = re.sub(r'/{2,}', '/', url_path)      # ////////url/path?a=1   -->   /url/path?a=1
        return '{host}{connector}{path}'.format(host=host,
                                                connector='' if url_path.startswith('/') else '/',
                                                path=url_path)

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
                if _path_cnt_ > 50:
                    continue
                self.__urlpath_limit[urlpath] = _path_cnt_ + 1
            # 处理文件链接(文件过大下载较慢,影响爬取速度)
            filename = url_file(url)
            if self.filter(filename):
                continue
            if filename:
                self.file_urls[url] = self.all_urls.get(url)
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
                    self.all_urls[url] = '302'
                    self.all_urls[resp.url] = url
                    url = self.abspath(resp.url, site=self.site)  # 更新重定向后的URL
                    # 再次处理文件链接
                    filename = url_file(url)
                    if filename:
                        self.file_urls[url] = self.all_urls.get(url)
                        yield self.RespInfo(status_code=status_code, url=url, filename=filename, html_text=None, desc='')
                        continue
            # except (MissingSchema, InvalidURL, InvalidSchema, ConnectionError, ReadTimeout) as e:
            except Exception as e:
                logger.error('GET %s %s' % (url, e))
                self.broken_urls[url] = self.all_urls.get(url, '')
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
                if self.same_site and urlsite(new_url).reg_domain != self.site:
                    continue
                new_url = self.abspath(new_url, site=self.site)
                # 限制URL
                if path_limit and path_limit not in new_url:
                    continue
                if self.hsts and new_url.startswith('http://'):
                    new_url = 'https://' + new_url[7:]
                if new_url and new_url not in self.all_urls:
                    self.all_urls[new_url] = url  # 保存该new_url的来源地址
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

