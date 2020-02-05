# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/16
"""
import requests
from lxml import etree
from app.settings import HEADERS
__author__ = 'caijinxu'


def spider_pages(url):
    """爬取链接分页，通过页面下加 _2获取"""
    paging = []
    paging.append(url)
    urlp = url.rsplit('.', 1)
    pagenum = 2
    while True:
        try:
            pageurl = urlp[0] + "_" + str(pagenum) + "." + urlp[1]
            r = requests.get(pageurl, headers=HEADERS)
            if r.status_code == 200:
                paging.append(pageurl)
                pagenum += 1
            else:
                break
        except:
            break
    return paging


def spider_webimg(url, imgxpath, page):
    """爬取页面的图片链接"""
    paging = []
    if page:
        paging = spider_pages(url)
    else:
        paging.append(url)
    imgs = []
    for purl in paging:

        r = requests.get(purl, headers=HEADERS)
        selector = etree.HTML(r.content)
        pageimgs = selector.xpath(imgxpath)
        imgs += pageimgs
    imgs = list(set(imgs))
    return imgs

