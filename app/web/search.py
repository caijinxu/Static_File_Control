# -*- coding:utf-8 -*-
from flask import request, render_template
from . import web
from app.libs.es import EsObject
from app.view_models.article import ArticlesViewModel
from app.forms.article import SearchForm


# 查询文章，只能返回部分内容
@web.route('/article/', methods=['GET', 'POST'])
def article():
    form = SearchForm(request)
    list_article = []
    article_count = 0
    if request.method == 'POST' and form.validate():
        keyword = form.data['KeyWord']
        starttime = form.data['StartTime'] if form.data['StartTime'] else None
        stoptime = form.data['StopTime'] if form.data['StopTime'] else None
        es = EsObject()
        result = es.search_article_content(keyword, starttime, stoptime, 0, 5)
        article_count = es.total
        list_article = result[0]
        print(type(list_article))
        print(list_article)
    return render_template('article.html', form=form, list_article=list_article, article_count=article_count)


# 查询文章，返回所有内容
@web.route('/all_article/', methods=['GET', 'POST'])
def all_article():
    form = SearchForm(request)
    list_result = []
    count = 0
    if form.validate():
        es = EsObject()
        # 将查询参数保存
        es.set_attrs(form.data)
        es.help_article_content()
        generator_result = es.res
        articles = ArticlesViewModel()
        articles.save(generator_result, form.data)
        count = articles.total
        list_result = articles.articles
    return render_template('all_result.html', form=form, result=list_result, count=count)
