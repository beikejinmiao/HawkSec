#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import platform

Platform = platform.system().lower()
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
