#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from libs.enums import SENSITIVE_FLAG
from modules.interaction.manager import TaskManager

# target = 'https://eco.btbu.edu.cn/tzgg/86177.htm'
target = 'https://www.btbu.edu.cn/'
sensitive_flags = [SENSITIVE_FLAG.URL, ]


if __name__ == '__main__':
    task_manager = TaskManager(target, sensitive_flags)
    try:
        task_manager.start()
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass


