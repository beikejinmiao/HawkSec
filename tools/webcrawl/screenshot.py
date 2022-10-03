#!/usr/bin/env python  
# -*- coding:utf-8 _*-
import os
import pandas as pd
import hashlib
from collections import namedtuple
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from conf.paths import DUMP_HOME, TOOLS_HOME
from libs.logger import logger

"""
https://chromedriver.chromium.org/downloads
ChromeDriver 104.0.5112.79
注意：chromedriver.exe必须和安装的Chrome大版本保持一致
"""


PICTURE_HOME = os.path.join(DUMP_HOME, 'pictures')
if not os.path.exists(PICTURE_HOME):
    os.makedirs(PICTURE_HOME)

ScreenStat = namedtuple('ScreenStat', ['url', 'status_code', 'desc', 'picture_path'])


def md5(content):
    m = hashlib.md5()
    m.update(content.encode('utf-8'))
    return m.hexdigest()


def __webshot(url):
    # 初始化谷歌浏览器实例
    chrome_driver = os.path.join(TOOLS_HOME, 'webcrawl', 'chromedriver.exe')
    broswer = webdriver.Chrome(service=Service(chrome_driver))
    broswer.maximize_window()
    #
    try:
        broswer.get(url)
        site = urlparse(url).netloc
        picture_path = os.path.join(PICTURE_HOME, '%s-%s.png' % (site, md5(url)))
        broswer.get_screenshot_as_file(picture_path)
    except WebDriverException as e:
        exception_msg = str(e)
        if 'Stacktrace:' in exception_msg:
            exception_msg = exception_msg[:exception_msg.index('Stacktrace:')]
        exception_msg = exception_msg.replace('\n', '\t')
        return ScreenStat(url=url, status_code=0, desc=exception_msg, picture_path='')
    except Exception as e:
        return ScreenStat(url=url, status_code=0, desc=str(e), picture_path='')
    finally:
        broswer.quit()
    return ScreenStat(url=url, status_code=1, desc='success', picture_path=picture_path)


def webshot(urls):
    if isinstance(urls, str):
        urls = [urls]
    else:
        urls = sorted(set(urls))
    #
    url_pic_paths = dict()
    for url in urls:
        stat = __webshot(url)
        url_pic_paths[url] = stat
        logger.info(url + '' + stat.desc)
    return url_pic_paths


def hyperlink(value):
    # https://stackoverflow.com/questions/31820069/add-hyperlink-to-excel-sheet-created-by-pandas-dataframe-to-excel-method
    if not isinstance(value, str):
        raise ValueError('hyper link in excel must be string.')
    if not value:
        return ''
    return '=HYPERLINK("%s", "%s")' % (value, os.path.basename(value))


if __name__ == '__main__':
    df = pd.read_csv(os.path.join(DUMP_HOME, '敏感内容来源统计.csv'))
    _url_pic_paths = webshot(df['敏感内容'].values)
    df_pic = pd.DataFrame([item._asdict() for item in _url_pic_paths.values()])
    df_pic['picture_path'] = df_pic['picture_path'].apply(lambda x: hyperlink(x))
    df_pic.to_excel(os.path.join(DUMP_HOME, '外链URL网站截图.xlsx'), index=False)

    # photo('https://www.cybj.cn')          # 提示不是私密连接,需手动点击前往,不会自动跳转,截图只有等待跳转页面
    # photo('www.baidu.com')                # 没有协议前缀会报错: invalid argument
    # photo('http://zs.canvard.net.cn/')    # 抛出TimeoutException异常



