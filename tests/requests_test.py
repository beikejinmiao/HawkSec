#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import requests

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Cookie': 'FSSBBIl1UgzbN7NO=5EaxIZy3d5T6gAD7atLwQTihVfh2SuLJlm8U3UppfFzf5cU9RbpZal_oacaGsBizhBCZpOjxyCaloOK2mjIf5tG; JSESSIONID=A64964671DDF69CD123F853E796DA616; FSSBBIl1UgzbN7NP=5Rl61lKpJTvgqqqDoudnsoa21sYrDgAve21lu2pc.yEMUVzKaqoEOO_feFpktDoO3Kb585gwEdmGUD6LL31U21k3etFgemhjkvAX_L364doNMg_7SBnfJheWFVjwoAfsohHms.v9wFoGk9LVPLfZYkCF8_.FRwfflI3SMRAj2pVDuS4BB14536e.Xay.IvOam1J1iu.inFnL0wJpsGAQRLzAaypudA7F9r7QOF42nLJDvVLP7s4_l0D.qkJFGiobkclB8FjXRBTME.EVy1gjpcc',
#     'Host': 'www.scu.edu.cn',
#     'Referer': 'https://www.scu.edu.cn/',
#     'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
# }
# 
# # url = 'http://yjsy.uibe.edu.cn/cms/common/downloadFile.jsp?id=DBCPDCDCDCDIDIDBCPCIDBCNDJDHCJLJPKLMMKLOKNLMMDMDLDNCNHNBKHNELKMFOANBPILHLNLALIDCDADCDACOHAGEGG'
# url = 'https://www.scu.edu.cn/'
# # resp = requests.head(url, timeout=10)
# # print(resp.content)
# resp = requests.get(url, headers=headers, timeout=10)
# print(resp.text)
# print(resp.headers)
# 


def with_session():
    url = 'https://xjxnfz.cauc.edu.cn/zxhz/20191113203302'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    session = requests.Session()
    print(time.time())
    resp = session.get(url, headers=headers, timeout=10)

    from modules.interaction.extractor import TextExtractor
    extractor = TextExtractor(sensitive_flags=[0, 1])
    print(extractor.extract(resp.text))

    print(time.time())
    print(session.cookies.get_dict())
    # print(resp.text)


if __name__ == '__main__':
    with_session()


