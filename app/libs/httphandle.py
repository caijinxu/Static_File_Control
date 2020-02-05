# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/5/31
"""
import requests
from urllib.parse import urlparse
__author__ = 'caijinxu'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/50.0.2661.102 Safari/537.36"}


def httphandle(url):
    try:
        response = requests.get(url, headers=headers, timeout=2, allow_redirects=False)
        code = response.status_code
        if code == 200:
            return True
        else:
            return False
    except Exception as e:
        print("请求链接失败：", e)
        return False


def findpages(parse):
    """传入一个链接的urlparse，查找可能的分页，返回一个链接组成的链接"""

    urllist = []
    url = "http://" + parse.netloc + parse.path
    # 确认链接可以访问
    if httphandle(url):
        urllist.append(url)
    else:
        return urllist
    pathlist = parse.path.split('.shtml')
    flag = True
    i = 2
    while flag:
        make_url = "http://" + parse.netloc + pathlist[0] + "_" + str(i) + ".shtml"
        if httphandle(make_url):
            urllist.append(make_url)
            i += 1
        else:
            return urllist


def pcto3g(url):
    """接收一个pc页链接，返回一个相应的3g页地址，如果没有返回空值"""
    parse = urlparse(url)
    path3ghead = parse.netloc.replace('.test.com', '').replace('.', '_')
    make_url = "http://3g.test.com/" + path3ghead + parse.path
    if httphandle(make_url):
        return make_url


def g3topc(parse):
    """传入一个3g链接的urlparse类，转为pc页面"""
    try:
        g3pathhead = parse.path.split('/')[1]
        pc_netloc_head = g3pathhead.replace('_', '.')
        makeurl = "http://" + pc_netloc_head + ".test.com" + parse.path.replace("/" + g3pathhead, '')
        if httphandle(makeurl):
            return makeurl
    except Exception:
        return

