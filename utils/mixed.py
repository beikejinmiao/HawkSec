#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import paramiko
import tldextract
from urllib.parse import urlparse
from datetime import datetime, timedelta
from collections import defaultdict


def tree():
    return defaultdict(tree)


def tree2list(tr):
    lists = list()

    def _tree2list(d, ls):
        for k, v in d.items():
            ls.append(k)
            if isinstance(v, dict):
                _tree2list(v, ls)
            else:
                lists.append(ls + [v])
            ls.pop(-1)

    _tree2list(tr, list())
    return lists


def cur_date(msec=False):
    if msec is True:
        return datetime.now().isoformat(timespec='milliseconds')
    return datetime.now().isoformat(timespec='seconds')


def human_timedelta(seconds):
    """
    https://gist.github.com/dhrrgn/7255361
    输入秒： 100000
    输出：   1天3小时46分40秒
    """
    delta = timedelta(seconds=seconds)
    d = dict(days=delta.days)
    d['hour'], rem = divmod(delta.seconds, 3600)
    d['min'], d['sec'] = divmod(rem, 60)

    if d['days'] > 0:
        fmt = '{days}天{hour}小时{min}分{sec}秒'
    elif d['hour'] > 0:
        fmt = '{hour}小时{min}分{sec}秒'
    elif d['hour'] > 0:
        fmt = '{min}分{sec}秒'
    else:
        fmt = '{sec}秒'

    return fmt.format(**d)


def ssh_accessible(host, port=22, username=None, password=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=username, password=password, timeout=1)
    return True
    # socket.timeout: timed out
    # paramiko.ssh_exception.AuthenticationException: Authentication failed.
    # paramiko.ssh_exception.AuthenticationException: Authentication timeout.   # auth_timeout=1


def auto_decode(text):
    if not isinstance(text, bytes):
        return text
    #
    for charset in ('utf-8', 'gbk'):
        try:
            return text.decode(charset)
        except UnicodeDecodeError:
            pass
    return None


def urlsite(url, tld=True):
    url = url.lower()
    site = ''
    if re.match(r'^\w+://', url):
        site = urlparse(url).netloc
    #
    ext = tldextract.extract(url)
    if tld is True:
        if ext.registered_domain != '':
            return ext.registered_domain
        elif site != '':
            return site
        else:
            return ''
    #
    site = ext.subdomain
    if ext.domain:
        site = site + ('.' if site else '') + ext.domain
    if ext.suffix:
        site = site + ('.' if site else '') + ext.suffix
    return site


if __name__ == '__main__':
    human_timedelta(10800)
