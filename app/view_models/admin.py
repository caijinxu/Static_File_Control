# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/29
"""
import logging
import json
import traceback
from app.models import db
from app.models.whiteimages import *
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy.orm import joinedload
from flask import current_app, flash
from flask_admin.babel import gettext, ngettext, lazy_gettext
from wtforms import fields
from wtforms import validators
from app.forms.base import BaseForm
from jinja2 import Markup

log = logging.getLogger("flask-admin.sqla")


__author__ = 'caijinxu'


class NewBaseView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        return False

    # 设置缩略图的
    def list_thumbnail(view, context, model, name):
        if not model.imgurl:
            return ''

        return Markup('<img class="img-responsive" src="%s"><div>%s</div>' % (model.imgurl, model.imgurl))

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        joins = {}
        count_joins = {}

        query = self.get_query().filter_by()
        count_query = self.get_count_query() if not self.simple_list_pager else None

        # Ignore eager-loaded relations (prevent unnecessary joins)
        # TODO: Separate join detection for query and count query?
        if hasattr(query, '_join_entities'):
            for entity in query._join_entities:
                for table in entity.tables:
                    joins[table] = None

        # Apply search criteria
        if self._search_supported and search:
            query, count_query, joins, count_joins = self._apply_search(query,
                                                                        count_query,
                                                                        joins,
                                                                        count_joins,
                                                                        search)

        # Apply filters
        if filters and self._filters:
            query, count_query, joins, count_joins = self._apply_filters(query,
                                                                         count_query,
                                                                         joins,
                                                                         count_joins,
                                                                         filters)

        # Calculate number of rows if necessary
        count = count_query.scalar() if count_query else None

        # Auto join
        for j in self._auto_joins:
            query = query.options(joinedload(j))

        # Sorting
        query, joins = self._apply_sorting(query, joins, sort_column, sort_desc)

        # Pagination
        query = self._apply_pagination(query, page, page_size)

        # Execute if needed
        if execute:
            query = query.all()
        return count, query

    def delete_model(self, model):
        """
            Delete model.

            :param model:
                Model to delete
        """
        try:
            self.on_model_delete(model)
            self.session.flush()
            model.status = 1
            # self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to delete record.')

            self.session.rollback()

            return False
        else:
            self.after_model_delete(model)

        return True


# class WorkerInfoModelView(NewBaseView):
#     column_labels = {
#         'id': u'序号',
#         'workername': u'节点名称',
#         'remark': u'备注',
#         'create_time': u'创建时间'
#     }
#     column_list = ("id", "workername", "remark")
#     form_excluded_columns = ['create_time', 'status']
#     column_exclude_list = ['create_time', ]
#     create_modal = True
#     edit_modal = True
#
#
# workinfoview = WorkerInfoModelView(WorkerInfo, db.session)
#
#
# class ConfigInfoModelView(NewBaseView):
#
#     def config_validator(form, field):
#         # 列wtform验证
#         try:
#             json.loads(field.data)
#         except:
#             raise validators.ValidationError("json格式错误" + traceback.format_exc())
#     column_labels = {
#         'id': u'序号',
#         'config': u'json格式配置信息',
#         'remark': u'备注',
#         'name': u'配置名称',
#         "updatetime": u'更新时间',
#         "create_time": "创建时间"
#     }  # 列名称对应别名
#     form_excluded_columns = ['create_time', 'status', "updatetime", "configinfo"] # 从列表视图中隐藏列
#     column_list = ("id", "name", "config", "remark", "updatetime", "create_time")  # 列表视图展示
#     column_editable_list = ['name', 'config', "remark"]  # 可以编辑的列
#     create_modal = True  # 添加和编辑表单显示在列表页面上的模态窗口中，而不是专用的创建和编辑页面
#     edit_modal = True  # 添加和编辑表单显示在列表页面上的模态窗口中，而不是专用的创建和编辑页面
#     form_args = {
#         "config":{
#             "validators": [config_validator]
#         }
#     }  # 使用wtform数据验证
# configview = ConfigInfoModelView(ConfigInfo, db.session, endpoint='testendpoint')


class WhiteImageModelView(NewBaseView):
    column_labels = {
        "imgurl": "图片链接",
        "remark": "备注",
        "create_time": "创建时间"
    }
    column_list = ("imgurl", "remark", "create_time")  # 列表显示
    column_editable_list = ["remark"]  # 可以编辑的列
    edit_modal = True
    create_modal = True
    form_excluded_columns = ['create_time', 'status']  # 从列表视图中隐藏列
    column_searchable_list = ['imgurl']
    # 格式化列表的图像显示
    column_formatters = {
        'imgurl': NewBaseView.list_thumbnail
    }
whithimageview = WhiteImageModelView(WhiteImage, db.session, name="单独图片白名单", endpoint='whiteimage')


class WhiteWebImageModelView(NewBaseView):
    can_create = False
    can_edit = False
    column_searchable_list = ['imgurl', "whiteweb.url"]
    column_labels = {
        "imgurl": "图片链接",
        "whiteweb.remark": "备注",
        "create_time": "创建时间",
        "whiteweb.url": "来源页面链接"
    }
    column_list = ("imgurl", "whiteweb.url", "whiteweb.remark", "create_time")
    form_excluded_columns = ['create_time', 'status']  # 从列表视图中隐藏列
    # 格式化列表的图像显示
    column_formatters = {
        'imgurl': NewBaseView.list_thumbnail
    }
whitewebimgview = WhiteWebImageModelView(WhiteWebImg, db.session, name="白名单页面获取的图片", endpoint='whitewebimage')


class WhiteChannleImageModelView(NewBaseView):
    # 格式化列表的图像显示
    can_create = False
    can_edit = False
    column_labels = {
        "imgurl": "图片链接",
        "whitechannel.remark": "备注",
        "create_time": "创建时间",
        "whitechannel.channel_url": "来源频道链接"
    }
    column_list = ("imgurl", "whitechannel.channel_url", "whitechannel.remark", "create_time")
    column_formatters = {
        'imgurl': NewBaseView.list_thumbnail
    }
    column_searchable_list = ['imgurl', "whitechannel.channel_url"]
whitechannelimgview = WhiteChannleImageModelView(WhiteChannelImg, db.session, endpoint="whitechannleimage")


class DailyWhiteWebimgModelView(NewBaseView):
    can_create = False
    can_edit = False
    column_list = ("imgurl", "dailywhiteweb.weburl", "dailywhiteweb.remark", )
    column_formatters = {
        'imgurl': NewBaseView.list_thumbnail
    }
    column_searchable_list = ['imgurl', "dailywhiteweb.weburl"]
    column_labels = {
        "imgurl": "图片链接",
        "dailywhiteweb.remark": "备注",
        "create_time": "创建时间",
        "dailywhiteweb.weburl": "来源频道链接"
    }
dailywhitewebimgview = DailyWhiteWebimgModelView(DailyWhiteWebimg, db.session, endpoint='dailywhitewebimg')


class RetentionImgModelView(NewBaseView):
    can_create = False
    can_edit = False
    column_list = ("imgurl", "weburl", "webcreatetime", "retentionchannel.channel_url", "retentionchannel.channel_name",
                   "retentionchannel.retention")
    column_searchable_list = ['imgurl', "weburl"]
    column_labels = {
        "imgurl": "图片链接",
        "weburl": "图片所在页面链接",
        "webcreatetime": "页面创建时间",
        "retentionchannel.channel_url": "频道地址",
        "retentionchannel.channel_name": "频道名",
        "retentionchannel.retention": "图片保留天数"
    }

    column_formatters = {
        'imgurl': NewBaseView.list_thumbnail
    }
retentionimgview = RetentionImgModelView(RetentionImg, db.session, endpoint='retentimeimg')
