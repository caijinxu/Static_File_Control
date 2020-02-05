# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/5/30
"""
from flask import request
from app.web import web
from app.forms.api import ArticleForm
from app.view_models.api_view import api_urllist, send_url_etcd
from app.libs.error_code import ServerError

__author__ = 'caijinxu'


@web.route('/api/article', methods=['POST'])
def article_api():
    form = ArticleForm(request)
    try:
        if form.validate_for_api():
            urllist = api_urllist(form)
            return send_url_etcd(urllist, form)
    except:
        return ServerError(msg="服务端错误，请联系技术人员处理")



