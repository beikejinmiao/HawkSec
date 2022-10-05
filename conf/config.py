#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import socket
import platform

Platform = platform.system().lower()
RuntimeEnv = 'exe' if hasattr(sys, "_MEIPASS") else 'dev'

#
TIKA_SERVER_HOST = 'localhost'
TIKA_SERVER_PORT = 9998
TIKA_SERVER_URL = 'http://%s:%s/' % (TIKA_SERVER_HOST, TIKA_SERVER_PORT)
TIKA_SERVER_ACTIVE = False
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((TIKA_SERVER_HOST, TIKA_SERVER_PORT))
    if result == 0:
        TIKA_SERVER_ACTIVE = True
    sock.close()
except:
    pass

#
http_headers = {
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}
