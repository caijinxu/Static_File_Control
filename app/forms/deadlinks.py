# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/5/13
"""
from wtforms.fields import simple
from wtforms import validators, BooleanField
from wtforms import widgets
from wtforms.fields import core
from app.forms.base import BaseForm, DataRequired

__author__ = 'caijinxu'


class DeadlinksForms(BaseForm):
    fileupload = simple.StringField(
        label="上传列表文件",
        widget=widgets.FileInput(),
        render_kw={'placeholder': 'form-control'},
    )
    imageurls = simple.StringField(
        label="链接地址",
        widget=widgets.TextArea(),
        render_kw={"placeholder": "输入死链地址以换行分隔", "rows": 10, 'class': 'form-control'}
    )
    remark = simple.StringField(
        label="备注",
        widget=widgets.TextInput(),
        render_kw={"placeholder": "本次操作说明，可不填写。", 'class': 'form-control'}
    )
