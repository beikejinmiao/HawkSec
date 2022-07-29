#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import magic
import mimetypes
from collections.abc import Iterable
from utils.filedir import traverse


def get_files(root):
    local_files = list()
    if isinstance(root, (str, bytes)):
        if not os.path.exists(root):
            return local_files
        if os.path.isdir(root):
            local_files = traverse(root)
        else:
            local_files.append(root)
    elif isinstance(root, Iterable):
        for item in root:
            local_files.extend(get_files(item))
    return local_files


if __name__ == '__main__':
    # print(get_files([r'D:\var', [r'D:\root\xdocker'], {r'D:\迅雷下载': ''}]))
    print(mimetypes.guess_type('test.conf'))
    print(mimetypes.guess_type('test.html'))
    print(mimetypes.guess_type('test.js'))
    print(mimetypes.guess_type('test.css'))
    print(mimetypes.guess_type('test.jsp'))
    print(mimetypes.guess_type('test.py'))
    print(magic.from_file(r'D:\ChromeDownloads\Centos-7.repo', mime=True))



