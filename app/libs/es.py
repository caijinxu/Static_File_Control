# -*- coding:utf-8 -*-
# 操作elasticsearch方法

from elasticsearch import helpers
from elasticsearch import Elasticsearch
from flask import current_app
import time


class EsObject:
    def __init__(self):
        self.ES_HOST = current_app.config['ES_HOST']
        self.ES_PORT = current_app.config['ES_PORT']
        self.es = Elasticsearch([{'host': self.ES_HOST, 'port': self.ES_PORT}])
        self.res = None
        self.total = 0
        self.KeyWord = ''
        self.StartTime = ''
        self.StopTime = ''
        self.Title = True
        self.Url = True
        self.Time = True

    # 查询所有内容匹配，默认返回一个生成器对象
    # def help_article_content(self, keyword=None, start_time=None, stop_time=None):
    def help_article_content(self, **kw):
        query = {"query": {
            "bool": {"must": {"match": {"content": self.KeyWord}},
                     "filter": {"range": {"time": {"gte": self.StartTime, "lte": self.StopTime}}}}}}
        self.res = helpers.scan(self.es, index="articlesearch", doc_type="fulltext", query=query)
        # list_article = self._save_result()
        # return list_article
        # return self.res

    # 查询所有标题匹配，默认返回一个生成器对象
    def help_article_title(self, keyword, start_time, stop_time):
        if start_time == None:
            start_time = '1970-01-01T08:00:00'
        if stop_time == None:
            stop_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        query = {"query": {
            "bool": {"must": {"match": {"title": keyword}},
                     "filter": {"range": {"time": {"gte": start_time, "lte": stop_time}}}}}}
        self.res = helpers.scan(self.es, index="articlesearch", doc_type="fulltext", query=query)
        # list_article = self._save_result()
        # return list_article
        # return self.res

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            # 判断当前这个对象是否包含名字叫key 的属性
            if hasattr(self, key):
                setattr(self, key, value)

    # 返回部分结果集，通过from 和size参数指定返回的条目
    def search_article_content(self, keyword, start_time, stop_time, start=None, size=None):
        if start_time == None:
            start_time = '1970-01-01T08:00:00'
        if stop_time == None:
            stop_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        if start == None:
            start = 0
        if size == None:
            size = 5
        query = {"from": start, "size": size, "query": {"bool": {"must": {"match": {"content": keyword}}, "filter": {
            "range": {"time": {"gte": start_time, "lte": stop_time}}}}}}
        result = Elasticsearch.search(self.es, index="articlesearch", doc_type="fulltext", body=query)
        self.res = result['hits']['hits']
        self.total = result['hits']['total']
        list_article = self._save_result()
        return list_article, self.total

    def search_article_title(self, keyword, start_time, stop_time, start=None, size=None):
        if start_time == None:
            start_time = '1970-01-01T08:00:00'
        if stop_time == None:
            stop_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        if start == None:
            start = 0
        if size == None:
            size = 5
        query = {"from": start, "size": size, "query": {"bool": {"must": {"match": {"title": keyword}}, "filter": {
            "range": {"time": {"gte": start_time, "lte": stop_time}}}}}}
        result = Elasticsearch.search(self.es, index="articlesearch", doc_type="fulltext", body=query)
        self.res = result['hits']['hits']
        self.total = result['hits']['total']
        list_article = self._save_result()
        return list_article, self.total

    def _save_result(self):
        list_article = []
        for article in self.res:
            dict_article = {}
            dict_article['title'] = article['_source']['title']
            dict_article['url'] = article['_source']['url']
            dict_article['time'] = article['_source']['time']
            list_article.append(dict_article)
        return list_article

    # 判断
    def _test_argument(self, dict_argument):
        pass

