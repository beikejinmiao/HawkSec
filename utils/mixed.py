#!/usr/bin/env python
# -*- coding:utf-8 -*-
import paramiko
from datetime import datetime
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


def ssh_accessible(host, port=22, username=None, password=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=username, password=password, timeout=1)
    return True
    # socket.timeout: timed out
    # paramiko.ssh_exception.AuthenticationException: Authentication failed.
    # paramiko.ssh_exception.AuthenticationException: Authentication timeout.   # auth_timeout=1

