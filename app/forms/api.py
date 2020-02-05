# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/5/30
"""
from app.forms.base import BaseForm, DataRequired
from wtforms.fields import core
from wtforms.fields import simple
from app.libs.error_code import ParameterException
import traceback
import re
from urllib.parse import urlparse

__author__ = 'caijinxu'


class ArticleForm(BaseForm):
    handlemod = core.RadioField(
        label='选择操作类型',
        choices=(
            (1, '恢复链接'),
            (2, '删除链接'),
        ),
        validators=[DataRequired()],
        coerce=int
    )
    urls = simple.StringField(
        label="链接地址",
        validators=[DataRequired()],
    )
    remark = simple.StringField(
        label="备注",
    )
    relation = core.RadioField(
        label='是否关联3g网及分页',
        choices=(
            (1, '关联'),
            (2, '不关联'),
        ),
        validators=[DataRequired()],
        coerce=int
    )
    username = simple.StringField(
        label='用户名',
        validators=[
            DataRequired()
        ]
    )

    def validate_urls(self, field):
        try:
            for url in field.data.split():
                if not re.match('^http://', url):
                    raise ParameterException(url + '链接地址请以http://开头')
                parse = urlparse(url)
                if not re.search("test.com$", parse.netloc):
                    raise ParameterException(msg="只接收test.com域名下的链接")
        except:
            raise ParameterException("urls参数格式错误" + traceback.format_exc())

