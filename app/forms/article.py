# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/6/4
"""
from app.forms.base import BaseForm, DataRequired
from wtforms import  StringField, IntegerField,  SubmitField, BooleanField
from wtforms.validators import Length, NumberRange
__author__ = 'caijinxu'


class SearchForm(BaseForm):
    KeyWord = StringField(
        validators=[
            DataRequired(message='关键字不能为空'),
            Length(2, 20, message='关键字长度2到20')
        ],
        render_kw={
            "placeholder": "搜索关键字,长度2-20"
        }
    )
    StartTime = StringField(
        render_kw={
            "placeholder": "开始时间:2019-05-30T00:00:00"
        }
    )
    StopTime = StringField(
        render_kw={
            "placeholder": "结束时间:2019-05-30T13:00:00"
        }
    )
    Start = IntegerField(
        label='起始位置',
        default=0,
        validators=[
            NumberRange(min=0)
        ]
    )
    Size = IntegerField(
        label='数量',
        default=5,
        validators=[
            DataRequired(),
            NumberRange(min=1, max=100)
        ]
    )
    Title = BooleanField(
        label='标题',
        default=True
    )
    Time = BooleanField(
        label='时间',
        default=True
    )
    Url = BooleanField(
        label='url',
        default=True
    )
    submit = SubmitField('提交')