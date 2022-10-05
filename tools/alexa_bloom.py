#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import tldextract
from pybloom_live import BloomFilter
from utils.filedir import reader
from conf.paths import PRIVATE_RESOURCE_HOME
from conf.paths import ALEXA_BLOOM_FILTER_PATH


def create():
    bloom = BloomFilter(1000000, 0.001)
    for line in reader(os.path.join(PRIVATE_RESOURCE_HOME, 'alexa-top-30k.txt')):
        if line and not line.startswith('#'):
            bloom.add(line)
    for line in reader(os.path.join(PRIVATE_RESOURCE_HOME, 'whitedomain.txt')):
        if line and not line.startswith('#'):
            bloom.add(line)
    with open(ALEXA_BLOOM_FILTER_PATH, 'wb') as fopen:
        bloom.tofile(fopen)


def check(hosts):
    with open(ALEXA_BLOOM_FILTER_PATH, 'rb') as fopen:
        bloom = BloomFilter.fromfile(fopen)
    for host in hosts:
        host = host.lower()
        reg_domain = tldextract.extract(host).registered_domain
        if not reg_domain:
            reg_domain = host
        if reg_domain in bloom:
            print(reg_domain.ljust(30) + ' -> iswhite: true')
        else:
            print(reg_domain.ljust(30) + ' -> iswhite: unknown')


if __name__ == '__main__':
    domains = ['wifi.vivo.com.cn', 'vc-gp-n-105-242-216-26.umts.vodacom.co.za', 'info.lenovo.com.cn',
               'news.sina.com.cn', 'webapi.weather.com.cn', 'www.google.co.jp', 'www.google.com.hk',
               '71.am', 'connectivity.samsung.com.cn', '32.43.204.121.board.fz.fj.dynamic.163data.com.cn',

               'weibo.66.dnssina.com', 'mb.hd.sohu.com.cn', 'maps.google.co.jp', '1234567.com.cn', 'krypt.com',
               'alios.cn', 'www.fliggy.com', 'www.dingtalk.com', 'www.alibabagroup.com', 'www.alimama.com', 'www.xinmin.cn',
               'alitianji.com', 'alitelecom.com', 'baiduyundns.com', 'baidubos.com', 'samsungacr.com',
               'sogoubaidusm.cn', 'tencentbs.cn', 'huaweikyy.site', 'vivokyy.site']
    check(domains)

