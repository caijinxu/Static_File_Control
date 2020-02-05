# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/3
"""
from wtforms.fields import simple
from wtforms import validators, BooleanField
from wtforms import widgets
from wtforms.fields import core
from app.forms.base import BaseForm, DataRequired

__author__ = 'caijinxu'


class RecoverForms(BaseForm):
    handlemod = core.RadioField(
        label='选择操作类型',
        choices=(
            (1, '恢复链接'),
            (2, '删除链接'),
        ),
        validators=[DataRequired()],
        coerce=int
    )
    fileupload = simple.StringField(
        label="上传列表文件",
        widget=widgets.FileInput(),
        render_kw={'placeholder': 'form-control'},
    )
    imageurls = simple.StringField(
        label="链接地址",
        widget=widgets.TextArea(),
        render_kw={"placeholder": "输入链接url地址以换行分隔", "rows": 10, 'class': 'form-control'}
    )
    remark = simple.StringField(
        label="备注",
        widget=widgets.TextInput(),
        render_kw={"placeholder": "本次操作说明，可不填写。", 'class': 'form-control'}
    )
    addwhiteimg = core.RadioField(
        label='图片是否加入图片白名单',
        choices=(
            (0, '加入'),
            (1, '不加入')
        ),
        default=1,
        validators=[DataRequired()],
        coerce=int,
    )
    relation = core.RadioField(
        label='是否关联3g网及分页',
        choices=(
            (1, '关联'),
            (2, '不关联'),
        ),
        validators=[DataRequired()],
        coerce=int,
        default=2,
    )


class TaskInfoForm(BaseForm):
    taskid = simple.StringField(
        validators=[DataRequired()],
    )


class WebUrlForm(BaseForm):
    handlemod = core.RadioField(
        label='选择操作类型',
        choices=(
            (1, '恢复链接'),
            (2, '删除链接'),
        ),
        validators=[DataRequired()],
        coerce=int
    )
    weburls = simple.StringField(
        label="链接地址",
        widget=widgets.TextArea(),
        render_kw={"placeholder": "输入页面url地址以换行分隔", "rows": 10, 'class': 'form-control'},
        validators=[DataRequired()],
    )
    imagexpath = simple.StringField(
        label="获取图片的xpath规则",
        widget=widgets.TextInput(),
        render_kw={"placeholder": "爬取图片的xpath规则，不懂可以不填", "value": "//center//img/@src", 'class': 'form-control'}
    )

    pages = BooleanField(
        label="是否关联分页"
    )
    remark = simple.StringField(
        label="备注",
        widget=widgets.TextInput(),
        render_kw={"placeholder": "本次操作说明，可不填写。", 'class': 'form-control'}
    )


class FlushCDNFORM(BaseForm):
    imageurls = simple.StringField(
        label="刷新CND图片或目录地址",
        widget=widgets.TextArea(),
        render_kw={"placeholder": "输入图片或目录url地址以换行分隔", "rows": 10, 'class': 'form-control'},
        validators=[DataRequired()],
    )