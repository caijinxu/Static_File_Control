# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/5/13
"""
from flask import request, flash, url_for, render_template, redirect
from app.libs.etcd_handle import ETCD
from app.web import web
from app.forms.images import TaskInfoForm
from flask_login import login_required, current_user
from app.forms.deadlinks import DeadlinksForms
from app.view_models.deadlink_view import send_deadlink_etcd
from app.libs.mongo_conn import Mongo
from app.secure import DEADLINK_COLLECTION, MONGO_DATABASE
from app.view_models.images_view import get_pagination
import pymongo
import datetime
__author__ = 'caijinxu'


@web.route('/deadlinks', methods=['GET', 'POST'])
@login_required
def deadlinks():
    if request.method == "GET":
        form = DeadlinksForms(request)
        return render_template('deadlink/deadlink.html', form=form)
    else:
        filecontetn = ''
        if request.files.get('fileupload'):
            filecontetn = request.files['fileupload'].read()
        form = DeadlinksForms(request)
        urllist, tmpurllist ,turllist = [], [], []
        if filecontetn:
            filecontetn = str(filecontetn, encoding='utf-8')
            tmpurllist += filecontetn.split('\n')
            for tmpurl in tmpurllist:
                turllist += tmpurl.split('\r')
            for url in turllist:
                url = url.replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')
                if url:
                    urllist.append(url)
        if form.imageurls.data:
            urllist += form.imageurls.data.split('\n')
        urllist = list(set(urllist))
        # print(urllist)
        # return urllist
        if urllist:
            send_status = send_deadlink_etcd(urllist, form)
            if not send_status:
                return render_template('deadlink/deadlink.html', form=form)
            else:
                flash("任务下发完成，请勿重复发送任务")
                return redirect(url_for("web.deadhistory"))
        else:
            flash("请输入图片链接")
            return render_template('deadlink/deadlink.html', form=form)


@web.route('/deadhistory', methods=['GET'])
def deadhistory():
    page = int(request.args.get("page", 1))
    pagelimit = 20

    m = Mongo()
    mdb = m.client[MONGO_DATABASE]
    historytask = mdb[DEADLINK_COLLECTION].find({}, {"username": 1, "handlemod": 1, "createtime": 1, "webtaskinfo": 1,
                                                     "remark": 1, "taskuuid": 1}).sort("createtime",
                                                                                       pymongo.DESCENDING).\
        skip(pagelimit*(page - 1)).limit(pagelimit)
    taskcounts = mdb[DEADLINK_COLLECTION].find().count()
    pageination = get_pagination(taskcounts, pagelimit, page)
    return render_template('deadlink/deadhistory.html', historytask=historytask, pageination=pageination)


@web.route("/deadhistory/details", methods=['GET'])
def deadhistorydetails():
    page = int(request.args.get("page", 1))
    pagelimit = 100
    form = TaskInfoForm(request)
    if form.validate():
        m = Mongo()
        mdb = m.client[MONGO_DATABASE]
        # taskinfo = mdb[DEADLINK_COLLECTION].find_one({"taskuuid": form.taskid.data})
        tasks = mdb[DEADLINK_COLLECTION].aggregate(pipeline=[{"$match": {'taskuuid': form.taskid.data}},
                                                          {"$sort": {"urls": 1}},
                                                          {"$project": {"urls": 1, "_id": 0}},
                                                          {"$unwind": "$urls"}, {"$skip": pagelimit*(page - 1)},
                                                          {"$limit": pagelimit}])
        taskinfo = [task['urls'] for task in tasks]
        print(taskinfo)
        if taskinfo:
            # 处理Mongodb时区问题
            for urlinfo in taskinfo:
                for tinfo in urlinfo['taskinfo']:
                    if tinfo.get('updatetime'):
                        tinfo['updatetime'] = tinfo['updatetime'] + datetime.timedelta(hours=8)
            # 获取分页信息
            counts = mdb[DEADLINK_COLLECTION].aggregate(pipeline=[{"$match": {'taskuuid': form.taskid.data}},
                                                               {"$project": {'count': {"$size": "$urls"}}}])
            count = 1
            for c in counts:
                count = c["count"]
            pageination = get_pagination(count, pagelimit, page)
            return render_template('deadlink/historydetails.html', taskinfo=taskinfo, taskid=form.taskid.data,
                                   pageination=pageination)
        else:
            flash("没有查询到任务相关详情信息")
            return redirect(url_for('web.deadhistory'))
    else:
        flash("任务id错误")
        return redirect(url_for('web.deadhistory'))

