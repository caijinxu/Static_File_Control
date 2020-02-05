# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/5/31
"""
import uuid
import re
import time
import datetime
import json
from app.libs.mongo_conn import Mongo
from app.secure import MONGO_DATABASE, MONGO_COLLECTION
from app.libs.etcd_handle import ETCD
from urllib.parse import urlparse
from app.libs.httphandle import findpages, pcto3g, g3topc, httphandle
from app.libs.error_code import ServerError, Success, APIException
__author__ = 'caijinxu'


def api_urllist(form):
    """获取链接及相应关联链接"""
    urllist = []
    urls = form.urls.data.split()
    for url in urls:
        urllist.append(url)
        parse = urlparse(url)
        if form.relation.data == 1:  # 限制关联选项，查询分页，查询对应3gpc页
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
    return urllist


def send_url_etcd(urllist, form):
    e = ETCD()
    online_worker = e.get_online_worker()
    if not online_worker:
        return ServerError(msg="没有可以处理链接的worker节点，请确认链接正确和相应worker在线")
    img_url_roots = []
    for online in online_worker.values():
        img_url_roots += online.keys()
    taskuuid = str(uuid.uuid4())
    mlog = {
        "taskuuid": taskuuid,
        "handlemod": form.handlemod.data,
        "username": "api_" + form.username.data,
        "remark": form.remark.data,
        "createtime": datetime.datetime.now(),
        "urls": []
    }
    for imgurl in urllist:
        flag = 0
        imgurl = imgurl.rstrip('\n').rstrip('\r').replace(' ', '')
        for url_root in img_url_roots:
            if re.match(url_root, imgurl):

                flag = 1
                break
        urllog = {
            "url": imgurl,
            "taskinfo":[]
        }
        if flag == 0:
            urllog["taskinfo"].append({"status": "warning"})
        mlog["urls"].append(urllog)

    m = Mongo()
    mdb = m.client[MONGO_DATABASE]
    mdb[MONGO_COLLECTION].insert_one(mlog)
    # 将链接发送到etcd
    e.send_url_ectd(urllist, form.handlemod.data, taskuuid)
    time.sleep(1)  # 等1秒后，获取返回结果后返回
    taskinfo = mdb[MONGO_COLLECTION].find_one({"taskuuid": taskuuid})
    if taskinfo:
        # 处理Mongodb时区问题
        for urlinfo in taskinfo["urls"]:
            for tinfo in urlinfo['taskinfo']:
                if tinfo.get('updatetime'):
                    tinfo['updatetime'] = tinfo['updatetime'] + datetime.timedelta(hours=8)
                    tinfo['updatetime'] = tinfo['updatetime'].strftime('%Y-%m-%d %H:%M:%S')
        print(taskinfo)
        result = {
            'taskid': taskinfo["taskuuid"],
            'urlsinfo': taskinfo["urls"]
        }

        return Success(msg=json.dumps(result))
    else:
        return APIException(msg="获取任务处理历史出错，任务id：" + taskuuid)

