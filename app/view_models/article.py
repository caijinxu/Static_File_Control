# -*- coding:utf-8 -*-
from app.libs.es import EsObject


class ArticleViewModel:
    def __init__(self):

        self.Title = ''
        self.Url = ''
        self.Time = ''

    def cut_data(self, list_field, article):
        for field in list_field:
            field2 = field.lower()
            # print(type(field))
            # print(field, article['_source'][field])
            setattr(self, field, article['_source'][field2])
        # print(self.Title, self.Url, self.Time)
        return self


# 通过传入一个结果集的生成器对象，处理后再返回一个生成器
class ArticlesViewModel:
    def __init__(self):
        self.total = 0
        self.articles = []

    def save(self, result_generator, dict_field):
        list_field = self._fill_field(dict_field)
        self.articles = [ArticleViewModel().cut_data(list_field, article) for article in result_generator]
        self.total = len(self.articles)

    # 获得表单中要求输出的列
    def _fill_field(self, dict_field):
        list_tmp = []
        for key, value in dict_field.items():
            if value == True and key != 'submit':
                list_tmp.append(key)
        return list_tmp


