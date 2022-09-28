#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tika import parser as tikarser
from conf.paths import CONF_PATH

print(tikarser.from_file(CONF_PATH)["content"])


