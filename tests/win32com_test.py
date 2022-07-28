#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pythoncom
from libs.timer import timer
from tools.textract.office import ppt, pptx

# 线程中使用win32com发生错误
"""
  File "HawkSec\tools\textract\office.py", line 79, in ppt
    app = win32com.client.DispatchEx('Powerpoint.Application')
  File "HawkSec\venv\lib\site-packages\win32com\client\__init__.py", line 145, in DispatchEx
    dispatch = pythoncom.CoCreateInstanceEx(
pywintypes.com_error: (-2147221008, '尚未调用 CoInitialize。', None, None)
"""
# 解决方案： https://www.cnblogs.com/xcbb/p/15111276.html
"""
import pythoncom

def xxx():
    # 线程初始化
    pythoncom.CoInitialize()
    # 程序代码
    .....
    # 释放资源
    pythoncom.CoUninitialize()
"""


@timer(1, 5)
def extract():
    print(ppt(r'D:\ChromeDownloads\test.ppt'))
    print(pptx(r'D:\ChromeDownloads\test.pptx'))


if __name__ == '__main__':
    thread = extract()
    thread.join()


