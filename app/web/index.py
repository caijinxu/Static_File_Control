# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/9
"""
from flask import request, flash, url_for, render_template, redirect
from app.libs.etcd_handle import ETCD
from app.web import web

__author__ = 'caijinxu'



@web.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@web.route("/online_worker", methods=['GET'])
def online_worker():
    e = ETCD()
    workerinfo = e.get_online_recover_worker()
    if workerinfo:
        print(workerinfo)
        return render_template("online_worker.html", workerinfo=workerinfo)
    else:
        return render_template("online_worker.html")


