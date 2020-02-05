# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/3
"""
from flask import request, flash, url_for, render_template, redirect, jsonify, current_app
from flask_login import login_required, current_user
from app.web import web
from app.forms.images import RecoverForms, TaskInfoForm, WebUrlForm, FlushCDNFORM
from app.models.whiteimages import WhiteChannelImg, WhiteImage
from app.models.handleimages import HandleTask, HandleImgUrl
from app.libs.mongo_conn import Mongo
from app.view_models.images_view import send_url_etcd, send_webimg_etcd, send_cdn, get_pagination
from app.secure import MONGO_COLLECTION, MONGO_DATABASE
import pymongo
import traceback
import datetime
from math import ceil
__author__ = 'caijinxu'


@web.route('/url_handle', methods=['GET', 'POST'])
@login_required
def images_recover():
    if request.method == "GET":
        form = RecoverForms(request)
        return render_template('images/recoverimg.html', form=form)
    else:
        filecontetn = ''
        if request.files.get('fileupload'):
            filecontetn = request.files['fileupload'].read()
        form = RecoverForms(request)
        urllist, tmpurllist ,turllist = [], [], []
        if filecontetn:
            filecontetn = str(filecontetn, encoding='utf-8')
            tmpurllist += filecontetn.split('\n')
            for tmpurl in tmpurllist:
                turllist += tmpurl.split('\r')
            for url in turllist:
                url = url.replace('\n', '').replace('\r', '').replace(' ', '')
                if url:
                    urllist.append(url)
        if form.imageurls.data:
            urllist += form.imageurls.data.split('\n')
        urllist = list(set(urllist))
        if urllist:
            send_status = send_url_etcd(urllist, form)
            if not send_status:
                return render_template('images/recoverimg.html', form=form)
            else:
                flash("任务下发完成，请勿重复发送任务")
                return redirect(url_for("web.history"))
        else:
            flash("请输入图片链接")
            return render_template('images/recoverimg.html', form=form)


@web.route('/historytask', methods=['GET'])
def historytask():
    historytask = HandleTask.query.filter(HandleTask.status == 0).order_by(HandleTask.create_time.desc()).all()
    return render_template('images/historytask.html', historytask=historytask)


@web.route("/historytask/details", methods=['GET'])
def taskdetails():
    form = TaskInfoForm(request)
    if form.validate():
        taskinfos = HandleImgUrl.query.filter_by(taskid=form.taskid.data).all()
        if taskinfos:
            return render_template('images/taskdetails.html', taskinfos=taskinfos, taskid=form.taskid.data)
        else:
            flash("没有查询到任务相关详情信息")
            return redirect(url_for('web.historytask'))
    else:
        flash("任务id错误")
        return redirect(url_for('web.history'))


@web.route('/images/web', methods=['GET', 'POST'])
@login_required
def images_web():
    form = WebUrlForm(request)

    if request.method == 'POST' and form.validate():
        send_status = send_webimg_etcd(form)
        if not send_status:
            return render_template('images/web_img.html', form=form)
        else:
            flash("任务下发完成，请勿重复发送任务")
            return redirect(url_for("web.history"))
    else:
        return render_template('images/web_img.html', form=form)


@web.route("/flushcdn",  methods=['GET', 'POST'])
@login_required
def flush_cdn():
    """刷新cdn"""
    form = FlushCDNFORM(request)
    if request.method == "POST" and form.validate():
        imgurls = form.imageurls.data
        send_cdn(imgurls)
        return render_template("images/flush_cdn.html", form=form)
    else:
        return render_template("images/flush_cdn.html", form=form)


@web.route("/flushcdn_taskid",  methods=['GET'])
@login_required
def flush_cdn_taskid():
    if request.args.get("taskid"):
        taskimgs = HandleImgUrl.query.filter_by(taskid=request.args.get("taskid")).all()
        imageurls = ''
        for taski in taskimgs:
            imageurls += taski.imgurl + '\n'
        result = send_cdn(imageurls)
        return jsonify(result)
    else:
        return jsonify("dfef")


@web.route('/history', methods=['GET'])
def history():
    page = int(request.args.get("page", 1))
    pagelimit = 20

    m = Mongo()
    mdb = m.client[MONGO_DATABASE]
    historytask = mdb[MONGO_COLLECTION].find({}, {"username": 1, "handlemod": 1, "createtime": 1, "webtaskinfo": 1,
                                                  "remark": 1, "taskuuid": 1}).sort("createtime", pymongo.DESCENDING)\
        .skip(pagelimit*(page - 1)).limit(pagelimit)
    taskcounts = mdb[MONGO_COLLECTION].find().count()
    pageination = get_pagination(taskcounts, pagelimit, page)

    return render_template('images/history.html', historytask=historytask, pageination=pageination)


@web.route("/history/details", methods=['GET'])
def historydetails():
    page = int(request.args.get("page", 1))
    pagelimit = 100
    form = TaskInfoForm(request)
    if form.validate():
        m = Mongo()
        mdb = m.client[MONGO_DATABASE]
        # taskinfo = mdb[MONGO_COLLECTION].find_one({"taskuuid": form.taskid.data})
        tasks = mdb[MONGO_COLLECTION].aggregate(pipeline=[{"$match": {'taskuuid': form.taskid.data}},
                                                          {"$sort": {"urls": 1}},
                                                          {"$project": {"urls": 1, "handlemod": 1, "_id": 0}},
                                                          {"$unwind": "$urls"}, {"$skip": pagelimit*(page - 1)},
                                                          {"$limit": pagelimit}])
        taskinfo = {
            'urls': []
        }
        for task in tasks:
            taskinfo['handlemod'] = task['handlemod']
            taskinfo['urls'].append(task['urls'])
        if taskinfo:
            # 处理Mongodb时区问题
            for urlinfo in taskinfo['urls']:
                for tinfo in urlinfo['taskinfo']:
                    if tinfo.get('updatetime'):
                        tinfo['updatetime'] = tinfo['updatetime'] + datetime.timedelta(hours=8)
            # 获取分页信息
            counts = mdb[MONGO_COLLECTION].aggregate(pipeline=[{"$match":{'taskuuid': form.taskid.data}},
                                                          {"$project": {'count': {"$size": "$urls"}}}])
            count = 1
            for c in counts:
                count = c["count"]

            pageination = get_pagination(count, pagelimit, page)
            print(pageination)
            return render_template('images/historydetails.html', taskinfo=taskinfo, taskid=form.taskid.data,
                                   pageination=pageination)
        else:
            flash("没有查询到任务相关详情信息")
            return redirect(url_for('web.history'))
    else:
        flash("任务id错误")
        return redirect(url_for('web.history'))


@web.route("/flushcdn_taskuuid",  methods=['GET'])
@login_required
def flush_cdn_taskuuid():
    if request.args.get("taskuuid"):
        try:
            m = Mongo()
            mdb = m.client[MONGO_DATABASE]
            taskinfo = mdb[MONGO_COLLECTION].find_one({"taskuuid": request.args.get("taskuuid")})
            imageurls = ''
            for taski in taskinfo["urls"]:
                imageurls += taski["url"] + '\n'
            result = send_cdn(imageurls)
            return jsonify(result)
        except:
            return jsonify(traceback.format_exc())
    else:
        return jsonify("请发送taskuuid")