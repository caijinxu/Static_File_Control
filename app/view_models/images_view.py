# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/16
"""
import re
import time
import uuid
import json
from datetime import datetime
from flask import flash
from app.models import db
from app.models.handleimages import HandleTask, HandleImgUrl, CDNHandle
from app.models.whiteimages import WhiteImage
from flask_login import current_user
from app.libs.etcd_handle import ETCD
from app.libs.spider import spider_webimg
from app.libs.cdn_handle import cdn_handle
import traceback
from app.libs.mongo_conn import Mongo
from app.secure import MONGO_DATABASE, MONGO_COLLECTION
from math import ceil
from urllib.parse import urlparse
from app.libs.httphandle import findpages, pcto3g, g3topc, httphandle

__author__ = 'caijinxu'


# def send_url_etcd(urllist, form):
#     with db.auto_commit():
#         task = HandleTask()
#         task.handlemod = form.handlemod.data
#         task.username = current_user.username
#         task.remark = form.remark.data
#         db.session.add(task)
#     e = ETCD()
#     online_worker = e.get_online_recover_worker()
#     if not online_worker:
#         flash("没有可以出来图片链接的worker节点，请确认图片链接正确和相应worker在线")
#         # return render_template('images/recoverimg.html', form=form)
#         return False
#     img_url_roots = []
#     for online in online_worker.values():
#         img_url_roots += online.keys()
#     for imgurl in urllist:
#         flag = 0
#         imgurl = imgurl.rstrip('\n').rstrip('\r').replace(' ', '')
#         for url_root in img_url_roots:
#             if re.match(url_root, imgurl):
#                 if form.handlemod.data == 1:
#                     writekey = "/services/recoerjob/" + str(uuid.uuid4())
#                 else:
#                     writekey = "/services/deletejob/" + str(uuid.uuid4())
#                 lease = e.client.lease(30)
#                 e.client.put(writekey, imgurl.encode(), lease)
#                 flag = 1
#                 break
#         if flag == 0:
#             flash(imgurl + "：没有可以处理的worker，请确认链接格式")
#             with db.auto_commit():
#                 handimg = HandleImgUrl()
#                 handimg.imgurl = imgurl
#                 handimg.taskid = task.id
#                 handimg.taskstatus = 3
#                 db.session.add(handimg)
#         else:
#             with db.auto_commit():
#                 handimg = HandleImgUrl()
#                 handimg.imgurl = imgurl
#                 handimg.taskid = task.id
#                 db.session.add(handimg)
#         if form.addwhiteimg.data == 0:
#             try:
#                 with db.auto_commit():
#                     wimg = WhiteImage()
#                     wimg.imgurl = imgurl
#                     wimg.remark = form.remark.data
#                     wimg.create_time = time.strftime('%Y-%m-%d %H:%M:%S')
#                     db.session.add(wimg)
#             except:
#                 flash(imgurl + "加入图片白名单失败")
#     return True

def send_url_etcd(urls, form):
    e = ETCD()
    online_worker = e.get_online_worker()
    if not online_worker:
        flash("没有可以处理链接的worker节点，请确认链接正确和相应worker在线")
        return False
    img_url_roots = []
    for online in online_worker.values():
        img_url_roots += online.keys()
    taskuuid = str(uuid.uuid4())
    mlog = {
        "taskuuid": taskuuid,
        "handlemod": form.handlemod.data,
        "username": current_user.username,
        "remark": form.remark.data,
        "createtime": datetime.now(),
        "urls": []
    }
    urllist = []
    # 获取分页及关联3g页
    for url in urls:
        urllist.append(url)
        if form.relation.data == 1:  # 限制关联选项，查询分页，查询对应3gpc页
            parse = urlparse(url)
            if httphandle(url):
                if parse.netloc == "3g.test.com":
                    # 3g页，转为pc页再查询分页
                    pcurl = g3topc(parse)
                    if pcurl:
                        urllist.append(pcurl)
                        pcparse = urlparse(pcurl)
                        pcurls = findpages(pcparse)
                        if pcurls:
                            urllist = urllist + pcurls
                else:
                    # pc页面，查询分页再转为3g页
                    pcurls = findpages(parse)
                    if pcurls:
                        urllist = urllist + pcurls
                        for pcurl in pcurls:
                            g3url = pcto3g(pcurl)
                            if g3url:
                                urllist.append(g3url)
        urllist = list(set(urllist))

    for imgurl in urllist:
        flag = 0
        imgurl = imgurl.rstrip('\n').rstrip('\r').replace(' ', '')
        for url_root in img_url_roots:
            if re.match(url_root, imgurl):
                flag = 1
                break
        urllog = {
            "url": imgurl,
            "taskinfo": []
        }
        if flag == 0:
            flash(imgurl + "：没有可以处理的worker，请确认链接格式")
            urllog["taskinfo"].append({"status": "warning"})
        mlog["urls"].append(urllog)
        if form.addwhiteimg.data == 0:
            try:
                with db.auto_commit():
                    wimg = WhiteImage()
                    wimg.imgurl = imgurl
                    wimg.remark = form.remark.data
                    wimg.create_time = time.strftime('%Y-%m-%d %H:%M:%S')
                    db.session.add(wimg)
            except:
                flash(imgurl + "加入图片白名单失败")
    m = Mongo()
    mdb = m.client[MONGO_DATABASE]
    mdb[MONGO_COLLECTION].insert_one(mlog)
    # 将链接发送到etcd
    e.send_url_ectd(urllist, form.handlemod.data, taskuuid)
    # for imgurl in urllist:
    #     if form.handlemod.data == 1:
    #         writekey = "/services/recoerjob/" + str(uuid.uuid4())
    #     else:
    #         writekey = "/services/deletejob/" + str(uuid.uuid4())
    #     lease = e.client.lease(30)
    #     e.client.put(writekey, imgurl.encode(), lease)
    return True


# def send_webimg_etcd(form):
#     weblist = form.weburls.data.split('\n')
#     webimg = dict()
#     for weburl in weblist:
#         webimg[weburl] = spider_webimg(weburl, form.imagexpath.data, form.pages.data)
#     with db.auto_commit():
#         task = HandleTask()
#         task.handlemod = form.handlemod.data
#         task.username = current_user.username
#         task.remark = form.remark.data
#         task.webtaskinfo = json.dumps(webimg, sort_keys=True, indent=4, separators=(',', ': '))
#         db.session.add(task)
#     e = ETCD()
#     online_worker = e.get_online_recover_worker()
#     if not online_worker:
#         flash("没有可以出来图片链接的worker节点，请确认图片链接正确和相应worker在线")
#         # return render_template('images/recoverimg.html', form=form)
#         return False
#     urllist = []
#     for imgs in webimg.values():
#         urllist += imgs
#     urllist = list(set(urllist))
#     img_url_roots = []
#     for online in online_worker.values():
#         img_url_roots += online.keys()
#     for imgurl in urllist:
#         flag = 0
#         imgurl = imgurl.rstrip('\n').rstrip('\r').replace(' ', '')
#         for url_root in img_url_roots:
#             if re.match(url_root, imgurl):
#                 if form.handlemod.data == 1:
#                     writekey = "/services/recoerjob/" + str(uuid.uuid4())
#                 else:
#                     writekey = "/services/deletejob/" + str(uuid.uuid4())
#                 lease = e.client.lease(60)
#                 e.client.put(writekey, imgurl, lease)
#                 flag = 1
#         if flag == 0:
#             flash(imgurl + "：没有可以处理的worker，请确认链接格式")
#             with db.auto_commit():
#                 handimg = HandleImgUrl()
#                 handimg.imgurl = imgurl
#                 handimg.taskid = task.id
#                 handimg.taskstatus = 3
#                 db.session.add(handimg)
#         else:
#             with db.auto_commit():
#                 handimg = HandleImgUrl()
#                 handimg.imgurl = imgurl
#                 handimg.taskid = task.id
#                 db.session.add(handimg)
#     return True

def send_webimg_etcd(form):
    weblist = form.weburls.data.split('\n')
    webimg = dict()
    for weburl in weblist:
        weburl = weburl.rstrip('\n').rstrip('\r').replace(' ', '')
        webimg[weburl] = spider_webimg(weburl, form.imagexpath.data, form.pages.data)
    taskuuid = str(uuid.uuid4())
    mlog = {
        "taskuuid": taskuuid,
        "handlemod": form.handlemod.data,
        "username": current_user.username,
        "remark": form.remark.data,
        "createtime": datetime.now(),
        "webtaskinfo": json.dumps(webimg, sort_keys=True, indent=4, separators=(',', ': ')),
        "urls": []
    }
    e = ETCD()
    online_worker = e.get_online_worker()
    if not online_worker:
        flash("没有可以处理链接的worker节点，请确认链接正确和相应worker在线")
        return False
    urllist = []
    for imgs in webimg.values():
        urllist += imgs
    urllist = list(set(urllist))
    img_url_roots = []
    for online in online_worker.values():
        img_url_roots += online.keys()
    for imgurl in urllist:
        urllog = {
            "url": imgurl,
            "taskinfo": []
        }
        flag = 0
        imgurl = imgurl.rstrip('\n').rstrip('\r').replace(' ', '')
        for url_root in img_url_roots:
            if re.match(url_root, imgurl):
                flag = 1
                break
        if flag == 0:
            flash(imgurl + "：没有可以处理的worker，请确认链接格式")
            urllog["taskinfo"].append({"status": "warning"})
        mlog["urls"].append(urllog)
    m = Mongo()
    mdb = m.client[MONGO_DATABASE]
    mdb[MONGO_COLLECTION].insert_one(mlog)
    # 将图片链接发送到etcd
    e.send_url_ectd(urllist, form.handlemod.data, taskuuid)
    # for imgurl in urllist:
    #     if form.handlemod.data == 1:
    #         writekey = "/services/recoerjob/" + str(uuid.uuid4())
    #     else:
    #         writekey = "/services/deletejob/" + str(uuid.uuid4())
    #     lease = e.client.lease(60)
    #     e.client.put(writekey, imgurl, lease)
    return True


def send_cdn(imgurls):
    imgurllist = imgurls.split('\n')
    turllist = []
    for tmpurl in imgurllist:
        turllist += tmpurl.split('\r')
    urls, dirs = [], []
    for iurl in turllist:
        iurl = iurl.replace('\n', '').replace('\r', '').replace(' ', '')
        if iurl:
            if iurl[-1] == "/":
                dirs.append(iurl)
            else:
                urls.append(iurl)
    updata = {
        "urlAction": "expire"
    }
    if dirs:
        updata['dirs'] = dirs
    if urls:
        updata['urls'] = urls
    print(updata)
    if not dirs and not urls:
        flash("请求没有包含有效的链接地址")
        return "请求没有包含有效的链接地址"

    with db.auto_commit():
        cdnlog = CDNHandle()
        cdnlog.usename = current_user.username
        cdnlog.updata = json.dumps(updata)
        try:
            cdn_result = cdn_handle(updata)
            flash("成功发送刷新请求\nCDN返回结果：" + cdn_result)
            result = "CDN返回结果：" + cdn_result
            cdnlog.result = cdn_result
        except:
            flash("发送刷新请求出错，错误信息：" + traceback.format_exc())
            result = "发送刷新请求出错，错误信息：" + traceback.format_exc()
            cdnlog.result = traceback.format_exc()
        db.session.add(cdnlog)
    return result


def get_pagination(counts, pagelimit, page):
    """传入总数、分页大小、当前页，返回分页信息"""
    pages = ceil(counts / pagelimit)
    pageination = {}
    if pages > 1:
        pageination['page'] = page
        # 分页大于1，处理分页
        if page - 1 >= 1:
            pageination['previous'] = page - 1
        if page + 1 <= pages:
            pageination['next'] = page + 1
        pageination['pagelist'] = []
        for i in range(-2, 3):
            if 0 < page + i <= pages:
                pageination['pagelist'].append(page + i)
    return pageination

