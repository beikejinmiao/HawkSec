#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import shutil


folder = 'D:\\PycharmProjects\\HawkSec'
for root, dirs, filenames in os.walk(folder):
    if root.endswith('__pycache__'):
        print('remove', root)
        shutil.rmtree(root)
    for filename in filenames:
        filepath = os.path.join(root, filename)
        if os.path.exists(filepath) and re.match(r'\.py[co]$', filepath):
            os.remove(filepath)
            print('remove', filepath)

