#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests

# url = 'http://yjsy.uibe.edu.cn/cms/common/downloadFile.jsp?id=DBCPDCDCDCDIDIDBCPCIDBCNDJDHCJLJPKLMMKLOKNLMMDMDLDNCNHNBKHNELKMFOANBPILHLNLALIDCDADCDACOHAGEGG'
url = 'http://yjsy.uibe.edu.cn/cms/common/rtfeditor/openfile.jsp?id=DBCPDCDCDDDGDHDECPNBOOMLKMCOGNHADE'
resp = requests.head(url, timeout=10)
print(resp.content)
print(resp.headers)

