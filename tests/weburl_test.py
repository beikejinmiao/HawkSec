#!/usr/bin/env python
# -*- coding:utf-8 -*-
from libs.web.url import urlsite
from libs.web.page import pagetitle, find_a_href

data = [
    'https://123/asds', 'sftp://www.baidu.com/asds', 'qwe://www.baidu.com/asds', 'https://1.1.1.1/asds'
    '1.1.1.1/asds', 'www.baidu.com/asds', 'host/asds'
]

for item in data:
    print(item)
    print('>>', urlsite(item))


url = 'https://www.bch.com.cn'
# resp = requests.get(url, headers=headers)
test_html1 = """
 <a href="https://www.stjude.org/ " target="_blank">美国圣裘德儿童研究医院</a></p>
 </li>
 <li><a href="https://chicagomedicalcenter.com/ " >
 </a>
 <p>
 <a href="https://chicagomedicalcenter.com/ " target="_blank">美国芝加哥大学医学中心</a></p>
 </li>
 <li><a href="http://www.ucla.edu/ " >
 </a>
 <p>
 <a href="http://www.ucla.edu/ " target="_blank">美国加州大学洛杉矶分校</a></p>
 </li>
 <li><a href="http://www.ufl.edu/ " >
 </a>
 <p>
"""

test_html2 = """
<!DOCTYPE html>
<html xmlns:wb="http://open.weibo.com/wb" lang="zh">
<body>
<head>
    <meta name="TileImage" content="http://p2.ifengimg.com/8cbe73a7378dafdb/2013/0416/logo.png">
    <script src="https://x0.ifengimg.com/fe/shank/content/2019/0418/fa.min.js" type="text/javascript"></script>
</head>
    <iframe src="https://www.w3schools.com"></iframe>
    <div style="background: url(https://www.w3schools.com/images/w3lynx_200.png)">
    <a href="https://www.google.com/search?q=lowsrc+dynsrc&newwindow=1&hl=zh-CN&sxsrf=-qQiuofrg%3A16&sclient=gws-wiz">凤凰纲</a>
    <!--<a href="http://www.jingduzhisheng.com/">京都之声</a>
    <a href="http://stu.chinacampus.org/">中国大学生年度人物评选</a>-->
    <div class="lefti">
        <a href="https://weibo.com/p/1002065293024672/home?is_all=1"><img src="./images/0508wb.png" />关注官方微博</a>
    </div>
</body>
</html>
"""

print(find_a_href(test_html1))
print(find_a_href(test_html2))
print(find_a_href(test_html2, regex=True))
print(pagetitle('https://www.baidu.com/'))
print(pagetitle('https://chicagomedicalcenter.com/'))

