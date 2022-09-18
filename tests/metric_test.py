#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from libs.pyaml import configure
from modules.interaction.metric import AbstractMetric


def _set_metric(metric=None):
    if not metric:
        metric = AbstractMetric()
        for key, value in configure['metric'].items():
            setattr(metric, key, value)
    if hasattr(metric, 'expend_time'):
        seconds = 0
        items = re.findall(r'\d+', metric.expend_time)
        bases = [1, 60, 3600, 86400]
        for i, item in enumerate(reversed(items)):
            seconds += int(item) * bases[i]
        print(seconds, '秒')
    print(metric)


if __name__ == '__main__':
    _set_metric()
