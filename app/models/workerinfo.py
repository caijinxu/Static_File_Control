# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/28
"""
from app.models.base import Base, db
from sqlalchemy import Column, String, Text, SmallInteger, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView

__author__ = 'caijinxu'


class ConfigInfo(Base):
    __tablename__ = "configinfo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    config = Column(Text, nullable=False, comment="json格式配置信息")
    name = Column(String(50), nullable=False,comment="配置名称")
    updatetime = Column(DATETIME, comment="更新时间")
    remark = Column(Text, nullable=True, comment='备注')
    username = Column(String(50), comment='操作人')
    __mapper_args__ = {"order_by": Base.create_time.desc()}
    @property
    def updatetime_datetime(self):
        if self.updatetime:
            return self.updatetime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return None

class WorkerInfo(Base):
    __tablename__ = "workerinfo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    workername = Column(String(50), nullable=False, comment="节点名称")
    remark = Column(Text, nullable=True, comment='备注')
    config_id = Column(Integer, ForeignKey("configinfo.id"))
    config = relationship("ConfigInfo", backref='configinfo')
    __mapper_args__ = {"order_by": Base.create_time.desc()}




