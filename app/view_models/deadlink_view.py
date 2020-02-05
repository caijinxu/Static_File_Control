# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/5/13
"""
import re
import time
import uuid
import json
from datetime import datetime
from flask import flash
from flask_login import current_user
from app.models import db
from app.libs.etcd_handle import ETCD
import traceback
from app.libs.mongo_conn import Mongo
from app.secure import MONGO_DATABASE, DEADLINK_COLLECTION
from app.settings import DEADLINKSDIR
__author__ = 'caijinxu'


def send_deadlink_etcd(urllist, form):
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
        "username": current_user.username,
        "remark": form.remark.data,
        "createtime": datetime.now(),
        "urls": []
    }
    for deadlink in urllist:
        flag = 0
        deadlink = deadlink.rstrip('\n').rstrip('\r').replace(' ', '')
        for url_root in img_url_roots:
            if re.match(url_root, deadlink):

                flag = 1
                break
        urllog = {
            "url": deadlink,
            "taskinfo":[]
        }
        if flag == 0:
            flash(deadlink + "：没有可以处理的worker，请确认链接格式")
            urllog["taskinfo"].append({"status": "warning"})
        mlog["urls"].append(urllog)
    m = Mongo()
    mdb = m.client[MONGO_DATABASE]
    mdb[DEADLINK_COLLECTION].insert_one(mlog)
    # 将链接发送到etcd
    # e.send_url_ectd(urllist, form.handlemod.data, taskuuid)
    for deadlink in urllist:
        writekey = DEADLINKSDIR + str(uuid.uuid4())
        lease = e.client.lease(30)
        task = {
            "taskuuid": taskuuid,
            "url": deadlink.replace('\n', '').replace('\r', '').replace(' ', '')
        }
        e.client.put(writekey, json.dumps(task), lease)
    return True