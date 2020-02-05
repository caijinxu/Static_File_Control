# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/30
"""
import json
import traceback
from wtforms.fields import simple
from wtforms import validators, BooleanField
from wtforms import widgets
from wtforms.fields import core
from app.forms.base import BaseForm, DataRequired

__author__ = 'caijinxu'


class ConfigForms(BaseForm):
    name = simple.StringField(
        label="配置名称",
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )

    config = simple.StringField(
        label="详细配置",
        widget=widgets.TextArea(),
        render_kw={"placeholder": "JSON格式的配置信息", "rows": 10, 'class': 'form-control'},
        validators=[DataRequired()]
    )

    remark = simple.StringField(
        label="备注",
        render_kw={"placeholder": "可不填写。", 'class': 'form-control'}
    )

    def validate_config(self, field):
        try:
            json.loads(field.data)
        except:
            raise validators.ValidationError("json格式错误" + traceback.format_exc())


class EditConfigForms(ConfigForms):

    name = simple.StringField(
        label="配置名称",
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'readonly': 'ture'}
    )


class WorkerForm(BaseForm):

    name = simple.StringField(
        label="节点名称",
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    remark = simple.StringField(
        label="备注",
        render_kw={"placeholder": "可不填写。", 'class': 'form-control'}
    )

    config = core.SelectMultipleField(
        label='选择配置',
        render_kw={'class': 'form-control'},
        coerce=int
    )

    def __init__(self, *args, **kwargs):
        from app.view_models.worker_view import worker_choices
        super(WorkerForm, self).__init__(*args, **kwargs)
        self.config.choices = worker_choices()

