# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/30
"""
import json
import traceback
from app.web import web
from datetime import datetime
from flask import request, flash, url_for, render_template, redirect
from app.forms.workerconfig import ConfigForms, EditConfigForms, WorkerForm
from app.models import db
from app.models.workerinfo import ConfigInfo, WorkerInfo
from flask_login import login_required, current_user
from app.libs.etcd_handle import ETCD
from app.settings import CONFIG_DIR
from app.view_models.worker_view import worker_view
__author__ = 'caijinxu'


@web.route('/worker_config/create', methods=['GET', 'POST'])
@login_required
def create_config():
    form = ConfigForms(request)
    try:
        if request.method == "POST" and form.validate():
            with db.auto_commit():
                wconfig = ConfigInfo()
                config = json.loads(form.config.data)
                wconfig.config = json.dumps(config, sort_keys=True, indent=4, separators=(',', ': '))  # json格式化
                wconfig.name = form.name.data
                wconfig.remark = form.name.data
                wconfig.updatetime = datetime.now()
                wconfig.username = current_user.username
                db.session.add(wconfig)
            flash("添加配置信息成功")
            return redirect(url_for("web.list_config"))
    except:
        flash("添加信息错误：" + traceback.format_exc(-1))
    return render_template("worker/editconfig.html", form=form, title="创建配置信息")


@web.route('/worker_config/list', methods=['GET'])
def list_config():
    configs = ConfigInfo.query.filter_by().all()
    return render_template("worker/list_config.html", configs=configs)


@web.route('/worker_config/edit', methods=['GET', 'POST'])
@login_required
def edit_config():
    form = EditConfigForms(request)
    wconfig = ConfigInfo.query.filter_by(name=form.name.data).first()
    if request.method == "POST" and form.validate():
        with db.auto_commit():
            config = json.loads(form.config.data)
            wconfig.config = json.dumps(config, sort_keys=True, indent=4, separators=(',', ': '))  # json格式化
            print(wconfig.config)
            wconfig.name = form.name.data
            wconfig.remark = form.name.data
            wconfig.updatetime = datetime.now()
            wconfig.username = current_user.username
        flash("修改配置信息成功")
        return redirect(url_for('web.list_config'))
    else:
        if not form.config.data:
            form.config.data = wconfig.config
            form.remark.data = wconfig.remark
            # form.name. = {'class': 'form-control', "readonly": "readonly"}
        return render_template("worker/editconfig.html", form=form, title="编辑")


@web.route('/worker_config/delete', methods=['POST'])
@login_required
def config_delete():

    if request.form.get("name"):
        wconfig = ConfigInfo.query.filter_by(name=request.form['name']).first()
        if wconfig:
            with db.auto_commit():
                wconfig.delete()
            flash("配置删除成功：" + request.form['name'])
            return "删除成功"
        else:
            return "没有相应配置信息"
    else:
        return "参数错误"


@web.route('/worker/create', methods=['GET', 'POST'])
@login_required
def create_worker():
    form = WorkerForm(request)
    if request.method == "POST" and form.validate():
        try:
            with db.auto_commit():
                worker = WorkerInfo()
                worker.workername = form.name.data
                worker.remark = form.remark.data
                # print(form.config.data)
                worker.config_id = form.config.data[0]
                db.session.add(worker)
            return redirect(url_for("web.list_worker"))
        except:
            flash("保存信息出错：" + traceback.format_exc(-1))
    return render_template("worker/editconfig.html", form=form, title="创建节点信息")


@web.route('/worker/list', methods=['GET'])
def list_worker():
    workers = WorkerInfo.query.filter_by().all()
    workerlist = worker_view(workers)
    return render_template("worker/list_worker.html", workerlist=workerlist)


@web.route('/worker/sendconfig', methods=['POST'])
@login_required
def sendconfig():
    print(request.form)
    if request.form.get("workername"):
        workerinfo = WorkerInfo.query.filter_by(workername=request.form['workername']).first()
        if workerinfo:
            config = {
                "config_name": workerinfo.config.name,
                "config": json.loads(workerinfo.config.config),
                "config_updatetime": workerinfo.config.updatetime.strftime("%Y-%m-%d %H:%M:%S")
            }
            config_key = CONFIG_DIR + workerinfo.workername
            print(config_key, config)
            e = ETCD()
            print(json.dumps(config))
            e.client.put(config_key, json.dumps(config))
            flash("配置下发成功")
            return ''
    flash("下发配置出错")
    return ''
