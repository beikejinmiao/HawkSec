#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from utils.refind import find_mobile


html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>北京科技大学大安全科学研究院</title>
</head>
<body>

    <!-- https://mss.ustb.edu.cn/tzgg/ca6467f74aa44748a7b42d4b7422558b.htm -->
    <section powered-by="xiumi.us" style="margin: 0px; padding: 0px 5px; outline: 0px; max-width: 100%; box-sizing: border-box; overflow-wrap: break-word !important; color: rgb(181, 59, 2); font-size: 14px; line-height: 1.8; letter-spacing: 1.8px;">
        <p style="margin: 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box; clear: both; min-height: 1em; overflow-wrap: break-word !important;">（会务） 黄冬梅：18857174982；<span style="letter-spacing: 1.8px;">张玮赟：13811790779</span></p>
        <p style="margin: 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box; clear: both; min-height: 1em; overflow-wrap: break-word !important;">（学术） 陈长坤：13187060583；<span style="letter-spacing: 1.8px;">吴建松：13466635893</span></p>
        <p style="margin: 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box; clear: both; min-height: 1em; overflow-wrap: break-word !important;">（财务） 杨立军：010-62793121,&nbsp;<span style="letter-spacing: 1.8px;">13641123132</span></p>
        <p style="margin: 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box; clear: both; min-height: 1em; overflow-wrap: break-word !important;">（网站） 刘晓栋：13681570688；<span style="letter-spacing: 1.8px;">徐 &nbsp;童：18374835358</span></p>
        <p style="margin: 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box; clear: both; min-height: 1em; overflow-wrap: break-word !important;">（合作） 姚浩伟：13937136590；<span style="letter-spacing: 1.8px;">胡啸峰：13401076812</span></p>
        <p style="margin: 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box; clear: both; min-height: 1em; overflow-wrap: break-word !important;">会务邮箱：conf@publicsafety.org.cn</p>
        <p style="margin: 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box; clear: both; min-height: 1em; overflow-wrap: break-word !important;"><strong style="margin: 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box; overflow-wrap: break-word !important;">注册网址：http://cpsc.publicsafety.org.cn</strong></p>
        <p style="margin: 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box; clear: both; min-height: 1em; overflow-wrap: break-word !important;">信息通知渠道：</p>
        <p style="margin: 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box; clear: both; min-height: 1em; text-indent: 2em; overflow-wrap: break-word !important;">微信公众号：</p>
    </section>


    <!-- https://kjy.ustb.edu.cn/zxdt/tzgg/a50b7e810b3a454ab7621eff311cbbfa.htm -->
    <p style="LINE-HEIGHT: 180%; text-indent: 2em; font-size: 14pt;"><span style="font-size: 16px; color: rgb(0, 0, 0);">报名联系人</span></p>
    <p style="LINE-HEIGHT: 180%; text-indent: 2em; font-size: 14pt;"><span style="font-size: 16px; color: rgb(0, 0, 0);">李 晋：13611226988</span></p>
    <p style="LINE-HEIGHT: 180%; text-indent: 2em; font-size: 14pt;"><span style="font-size: 16px; color: rgb(0, 0, 0);">祝赫锴：13581896338</span></p>


    <!-- https://faculty.ustb.edu.cn/ShengjunMiao/zh_CN/index/74275/list/index.htm -->
    <p>所在单位：土木与资源工程学院</p>
    <p>职务：土木与资源工程学院院长、党委副书记</p>
    <p>联系方式：移动电话：13671006571
    电子邮箱：miaoshengjun@163.com
    办公电话：010-62334954</p>


    <!-- https://faculty.ustb.edu.cn/XiubingHuang/zh_CN/jxcg/109485/list/index.htm -->
    <p>联系方式：13522249027</p>

    <!-- https://oice.ustb.edu.cn/xsgjjl/lxjl_/dqsxyx/index.htm -->
    <div>
        <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;line-height:125%;font-size:14pt"><span style="font-family:'times new roman';font-weight:bold">Supervisor’s Contacts</span></p>
        <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;line-height:125%;font-size:14pt"><span style="font-family:'times new roman'">Email: long.wang@ieee.org</span><span style="width:18.15pt;display:inline-block"> </span></p>
        <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;line-height:125%;font-size:14pt"><span style="font-family:'times new roman'">Tel.: +86-17611490612</span></p>
        <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;line-height:125%;font-size:14pt"><span style="font-family:'times new roman'">Fax: +86-10-62332931</span></p>
        <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;line-height:125%;font-size:14pt"><span style="font-family:'times new roman'"> </span></p>
        <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;line-height:125%;font-size:14pt"><span style="font-family:'times new roman';font-weight:bold"> </span></p>
    </div>


    <!-- https://www.ustb.edu.cn/tzgg/16849500.htm -->
    <div class="article art">
        <p style="text-indent:32.0pt;line-height:28.0pt;"><span style="font-family:仿宋;"><span style="font-size:18px;">根据《关于印发&lt;建设项目环境影响评价信息公开机制方案&gt;的通知》（环发〔2015〕162号）的要求，建设单位在建设项目环境影响报告书（表）编制完成后，向环境保护主管部门报批前，应当向社会公开环境影响报告书（表）全本。</span></span></p>
        <p style="text-indent:32.0pt;line-height:28.0pt;"><span style="font-family:仿宋;"><span style="font-size:18px;">现将《金属冶炼重大事故防控技术支撑基地环境影响报告表》公示如下：</span></span></p>
        <p style="text-indent:32.0pt;line-height:28.0pt;"><span style="font-family:仿宋;"><span style="font-size:18px;"><a href="../docs/20200924154521893801.pdf">../docs/20200924154521893801.pdf</a></span></span></p>
        <p align="left" style="text-align:left;text-indent:32.0pt;line-height:28.0pt;"><span style="font-family:仿宋;"><span style="font-size:18px;">联系人：阳建宏；联系方式：13683220990</span></span></p>
        <p align="right" style="text-align:right;text-indent:32.0pt;line-height:28.0pt;">&nbsp;</p>
        <p align="right" style="text-align:right;text-indent:32.0pt;line-height:28.0pt;"><span style="font-family:仿宋;"><span style="font-size:18px;">金属冶炼重大事故防控技术支撑基地筹建办公室</span></span></p>
        <p align="right" style="text-align:right;text-indent:32.0pt;line-height:28.0pt;"><span style="font-family:仿宋;"><span style="font-size:18px;">2020年9月24日&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></span></p>
    </div>

    <!-- https://news.ustb.edu.cn/info/1950/52088.htm -->
    <p style="margin-top: 0px; margin-bottom: 0px; padding: 16px 0px; border: 0px; overflow: hidden; list-style: none; line-height: 32px; font-family: 微软雅黑; font-size: medium; color: rgb(75, 75, 75); white-space: normal; background-color: rgb(255, 255, 255);">　　联系人及电话：王老师，022-23502579、13821740895。</p>
    <p style="margin-top: 0px; margin-bottom: 0px; padding: 16px 0px; border: 0px; overflow: hidden; list-style: none; line-height: 32px; font-family: 微软雅黑; font-size: medium; color: rgb(75, 75, 75); white-space: normal; background-color: rgb(255, 255, 255);">　　联系人及电话：陈老师，027-68754497、18062580285。</p>


    <!-- http://econ.ruc.edu.cn/gdpx1/kcyxbjw/index.htm -->
    <div class="detail">
      <p style="margin-top:0pt;margin-bottom:0pt;text-indent:32pt;text-align:justify;font-size:16pt"><span style="font-weight:bold"> </span></p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-indent:16pt;text-align:justify;font-size:16pt"><span style="font-weight:bold">北京校区</span><span style="font-size:12pt">联系人： &nbsp;</span></p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt">李老师 010-62513771 17778096570 (手机号码同微信号）</p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt">马老师 010-62515745 13269850470 (手机号码同微信号）</p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt">王老师 010-62516505 177188317705 (手机号码同微信号）</p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt">邮箱地址：ruc_li@ruc.edu.cn</p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt">报名地址：北京市海淀区中关村大街59号中国人民大学明德主楼956办公室</p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-indent:16pt;text-align:justify;font-size:16pt"><span style="font-weight:bold">苏州校区</span><span style="font-size:12pt">联系人：</span></p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt">王老师 13141865529 （手机号码同微信号）</p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt">邮箱地址： <a href="mailto:echo_wang@ruc.edu.cn" style="text-decoration:none" rel="nofollow"><span style="font-family:'calibri';font-size:10.5pt;color:#000000">echo_wang@ruc.edu.cn</span></a></p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt">报名地址：苏州工业园仁爱路158号中国人民大学苏州校区开太楼A区226室</p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-indent:16pt;text-align:justify;font-size:16pt"><span style="font-weight:bold">深圳校区</span><span style="font-size:12pt">联系人：</span></p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt"><span style="font-size:14px">司老师 0755-26548551 13537602071 （手机号同微信号）</span></p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt"><span style="font-size:14px">潘老师 &nbsp;17778181673（手机号同微信号）</span></p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt"><span style="font-size:14px">邮箱地址：ruczaizhi@ruc.edu.cn</span></p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-align:justify;font-size:12pt"><span style="font-size:14px">报名地址：深圳市南山区高新南四道19号虚拟大学园楼A501室（中国人民大学深圳研究院）</span></p>
      <p style="margin-top:0pt;margin-bottom:0pt;text-indent:16pt;text-align:justify;font-size:16pt"><br></p>
    </div>

    <!-- https://me.ustb.edu.cn/jiaoyujiaoxue/MEM/ -->
    <p>
        <span style="font-family: 宋体, SimSun; font-size: 18px;">薛老师:18515278616（微信同步） E-mail:</span>
        <a href="mailto:xxyoffice@ustb.edu.cn" style="text-decoration: underline; font-family: 宋体, SimSun; font-size: 18px;">
            <span style="font-family: 宋体, SimSun; font-size: 18px;">xxyoffice@ustb.edu.cn</span>
        </a>
    </p>


    <!-- https://mss.ustb.edu.cn/tzgg/f8166bbce71e4075b2e589b9b381899c.htm -->
    <p style="LINE-HEIGHT: 180%; text-indent: 2em; font-size: 14pt;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 宋大钊 18515139977；王 辉 18910003049</p>


    <!-- https://gc.ustb.edu.cn/fxljxjy/tzgga/e1e9e15cf88d414b9076fb51359527a7.htm -->
    <p style="margin-top:0pt; margin-bottom:0pt; text-indent:28pt; line-height:22pt; widows:0; orphans:0">
        <span style="font-family:华文楷体; font-size:14pt">手</span>
        <span style="font-family:华文楷体; font-size:14pt"> 机：18600869587（苏燕羽） </span>
        <span style="font-family:华文楷体; font-size:14pt">17611535838</span>
        <span style="font-family:华文楷体; font-size:14pt">（韩大海） </span>
    </p>
    
    
    <!-- https://gc.ustb.edu.cn/fxljxjy/tzgga/5a77beaab1f34d17aba101885e6f9328.htm -->
    <p style="margin-top:0pt; margin-left:31.5pt; margin-bottom:0pt; line-height:26pt; background-color:#ffffff">
        <span style="font-family:仿宋; font-size:16pt">中国钢铁工业协会 申永亮 李磊磊</span><br>
        <span style="font-family:仿宋; font-size:16pt">电话： 010—65135472</span><br>
        <span style="font-family:仿宋; font-size:16pt">北京科技大学继续教育学院 王</span>
        <span style="font-family:仿宋; font-size:16pt">玉敏</span>
        <span style="font-family:仿宋; font-size:16pt">、 韩老师</span>
        <span style="font-family:仿宋; font-size:16pt">、</span>
        <span style="font-family:仿宋; font-size:16pt">苏老师</span><br>
        <span style="font-family:仿宋; font-size:16pt">电话： 010-65749084</span><br>
        <span style="font-family:仿宋; font-size:16pt">手机： 13671189943（王</span>
        <span style="font-family:仿宋; font-size:16pt">玉敏</span>
        <span style="font-family:仿宋; font-size:16pt">）、 13621320304（韩大海）</span><br>
        <span style="font-family:仿宋; font-size:16pt; -aw-import:spaces"> </span>
        <span style="font-family:仿宋; font-size:16pt">18600869587</span>
        <span style="font-family:仿宋; font-size:16pt">（苏燕羽）</span>
    </p>

    
    <!-- https://info.ustb.edu.cn/wlaq/aqpx/b02af5a4ad984768a9839e2adf4a1876.htm -->
    <span style="font-size: 18px; font-family: 微软雅黑, &quot;Microsoft YaHei&quot;;">=A1.run(mobile=13800013800)</span>


    <!-- http://study.cqu.edu.cn/index/zxxx/xyzd/gxylxsbzrlxfs.htm -->
    <table align="center" border="1" cellspacing="0" cellpadding="0" style="width: 790px;">
     <thead>
      <tr class="firstRow">
       <th scope="col" style="width: 28px; height: 43px;"><p><strong>序号</strong></p></th>
       <th scope="col" style="width: 113px; height: 43px;"><p><strong>学院</strong></p></th>
       <th scope="col" style="width: 57px; height: 43px;"><p><strong>姓名</strong></p></th>
       <th scope="col" style="width: 28px; height: 43px;"><p><strong>性别</strong></p></th>
       <th scope="col" style="width: 85px; height: 43px;"><p><strong>办公室/联系电话</strong></p></th>
       <th scope="col" style="width: 94px; height: 43px;"><p><strong>手机号码</strong></p></th>
       <th scope="col" style="width: 180px; height: 43px;"><p><strong>办公地点</strong></p></th>
       <th scope="col" style="width: 180px; height: 43px;"><p><strong>邮箱</strong></p></th>
      </tr>
     </thead>
     <tbody>
      <tr>
       <td style="width: 28px; height: 48px;"><p style="text-align: center;">1</p></td>
       <td style="width: 113px; height: 48px;"><p style="text-align: center;">经济与工商管理学院</p></td>
       <td style="width: 57px; height: 48px;"><p style="text-align: center;">胡小容</p></td>
       <td style="width: 28px; height: 48px;"><p style="text-align: center;">女</p></td>
       <td style="width: 85px; height: 48px;"><p style="text-align: center;">65105710</p></td>
       <td style="width: 94px; height: 48px;"><p style="text-align: center;">15123380832</p></td>
       <td style="width: 180px; height: 48px;"><p style="text-align: center;">经管学院607</p></td>
       <td style="width: 180px; height: 48px;"><p style="text-align: center;"><a title="mailto:huxiaorong@cqu.edu.cn" href="mailto:huxiaorong@cqu.edu.cn">huxiaorong@cqu.edu.cn</a></p></td>
      </tr>
      <tr>
       <td style="width: 28px; height: 45px;"><p style="text-align: center;">2</p></td>
       <td style="width: 113px; height: 45px;"><p style="text-align: center;">公共管理学院</p></td>
       <td style="width: 57px; height: 45px;"><p style="text-align: center;">周聆</p></td>
       <td style="width: 28px; height: 45px;"><p style="text-align: center;">女</p></td>
       <td style="width: 85px; height: 45px;"><p style="text-align: center;">65102373</p></td>
       <td style="width: 94px; height: 45px;"><p style="text-align: center;">13594178033</p></td>
       <td style="width: 180px; height: 45px;"><p style="text-align: center;">公管学院212</p></td>
       <td style="width: 180px; height: 45px;"><p style="text-align: center;"><a title="mailto:mxzhouling@cqu.edu.cn" href="mailto:mxzhouling@cqu.edu.cn">mxzhouling@cqu.edu.cn</a></p></td>
      </tr>
      <tr>
       <td style="width: 28px; height: 47px;"><p style="text-align: center;">3</p></td>
       <td style="width: 113px; height: 47px;"><p style="text-align: center;">外国语学院</p></td>
       <td style="width: 57px; height: 47px;"><p style="text-align: center;">张文静</p></td>
       <td style="width: 28px; height: 47px;"><p style="text-align: center;">女</p></td>
       <td style="width: 85px; height: 47px;"><p style="text-align: center;">65678525</p></td>
       <td style="width: 94px; height: 47px;"><p style="text-align: center;">15823806864</p></td>
       <td style="width: 180px; height: 47px;"><p style="text-align: center;">外国语学院102</p></td>
       <td style="width: 180px; height: 47px;"><p style="text-align: center;"><a href="mailto:2579215768@qq.com">2579215768@qq.com</a></p></td>
      </tr>
      </tr>
     </tbody>

    <!-- https://career.fjnu.edu.cn/14/8c/c10194a332940/page.htm -->
    
    
    
</body></html>
"""

for item in find_mobile(html):
    print(item)





