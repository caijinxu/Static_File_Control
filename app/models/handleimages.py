# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/9
"""
from app.models.base import Base, db
from sqlalchemy import Column, String, Text, SmallInteger, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import relationship

__author__ = 'caijinxu'


class HandleTask(Base):
    __tablename__ = "handletask"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    handlemod = Column(Integer, nullable=False, comment='1：恢复图片，2：删除图片')
    remark = Column(String(255), nullable=True, comment='备注')
    webtaskinfo = Column(Text, nullable=True, comment='通过页面获取的图片链接，json格式')
    taskuuid = Column(String, nullable=False, comment="用于查找mongodb操作日志")


class HandleImgUrl(Base):
    __tablename__ = "handleimgurl"
    id = Column(Integer, primary_key=True, autoincrement=True)
    taskid = Column(Integer, ForeignKey('handletask.id'))
    updatetime = Column(DATETIME, comment="更新时间")
    imgurl = Column(String, nullable=False)
    taskstatus = Column(Integer, default=0, comment="1: 操作成功, 2: worker节点出错失败")
    task = relationship("HandleTask", backref='imgurl')
    remark = Column(Text, nullable=True, comment='备注')

    @property
    def updatetime_datetime(self):
        if self.updatetime:
            return self.updatetime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return None


class CDNHandle(Base):
    __tablename__ = "cdnhandlelog"
    id = Column(Integer, primary_key=True, autoincrement=True)
    updata = Column(Text, nullable=False, comment="上传CDN刷新参数")
    result = Column(Text, comment='CDN返回结果')
    usename = Column(String(50), comment='操作人')
