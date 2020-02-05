# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/4
"""
from app.models.base import Base, db
from sqlalchemy import Column, String, Text, SmallInteger, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import relationship

__author__ = 'caijinxu'


class WhiteImage(Base):
    """独立的白名单图片链接"""
    __tablename__ = "whiteimage"
    id = Column(Integer, primary_key=True, autoincrement=True)
    imgurl = Column(String(255), nullable=False, unique=True, comment='图片url地址')
    remark = Column(String(255), nullable=True, comment='备注')


class WhiteWeb(Base):
    """页面白名单"""
    __tablename__ = "whiteweb"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), nullable=False, unique=True, comment='白名单页面')
    paging = Column(Integer, default=0, comment="是否分页 0：不分页  1：分页")
    imagexpath = Column(String(255), default='//img/@src', comment='图片链接的xpath规则')
    pagexpath = Column(String(255), nullable=True, comment='翻页链接xpath规则')
    spidertime = Column(DATETIME, nullable=True, comment="最近一次爬取图片成功时间")
    remark = Column(String(255), nullable=True, comment='备注')


class WhiteWebImg(Base):
    """页面白名单对应的图片链接"""
    __tablename__ = "whitewebimg"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey("whiteweb.id"))
    imgurl = Column(String(255), nullable=False, unique=True, comment='图片url地址')

    whiteweb = relationship("WhiteWeb", backref='whitewebimg')


class WhiteChannel(Base):
    """设置为白名单的频道"""
    __tablename__ = "whitechannel"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_url = Column(String(255), nullable=False, unique=True, comment='频道链接')
    remask = Column(String(255), nullable=True, comment='备注')
    webxpath = Column(String(255), default='//a/@href', comment='爬取下级页面xpath规则')
    webimgxpath = Column(String(255), nullable=True, comment='爬取下级目录是如果此项不为空，爬取图片的xpath规则')
    imagexpath = Column(String(255), default='//img/@src', comment='爬取页面图片的规则')


class WhiteChannelWeb(Base):
    """白名单的频道爬取的页面"""
    __tablename__ = "whitechannelweb"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey('whitechannel.id'))
    weburl = Column(String, unique=True, nullable=True)
    spidertime = Column(DATETIME, nullable=True, comment="最近一次爬取图片成功时间")

    whitechannel = relationship("WhiteChannel", backref='whitechannelweb')


class WhiteChannelImg(Base):
    """白名单的频道爬取的图片"""
    __tablename__ = "whitechannelimg"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, nullable=True)
    imgurl = Column(String(255), nullable=False, unique=True, comment='图片url地址')
    channel_id = Column(Integer, ForeignKey('whitechannel.id'))
    whitechannel = relationship("WhiteChannel", backref='whitechannelimg')


class DailyWhiteWeb(Base):
    """频道首页或一些动态首页，每天爬取的图片地址删除，再重新爬取页面所有图片"""
    __tablename__ = "dailywhiteweb"
    id = Column(Integer, primary_key=True, autoincrement=True)
    weburl = Column(String, nullable=False)
    remark = Column(String(255), nullable=True, comment='备注')
    imagexpath = Column(String(255), default='//img/@src', comment='爬取页面图片的规则')


class DailyWhiteWebimg(Base):
    """内容每天清空，再通过爬虫重新获取，保证各频道首页图片不会被删除"""
    __tablename__ = "dailywhitiwebimg"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey('dailywhiteweb.id'))
    imgurl = Column(String)
    dailywhiteweb = relationship("DailyWhiteWeb", backref='dailywhitiwebimg')


class RetentionChannel(Base):
    """按照过期日期删除的频道"""
    __tablename__ = "retentionchannel"
    id = Column(Integer, primary_key=True, autoincrement=True)
    retention = Column(Integer, default='7', comment="频道内保留图片天数")
    channel_url = Column(String, comment="频道链接")
    channel_name = Column(String)
    imagexpath = Column(String(255), default='//img/@src', comment='爬取页面图片的规则')
    cms_catid = Column(String(255), comment='对content表catid')


class RetentionImg(Base):
    __tablename__ = "retentionimg"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey('retentionchannel.id'))
    webcreatetime = Column(DATETIME, comment='查询cms库中的createtime')
    imgurl = Column(String, comment='图片地址')
    weburl = Column(String)
    retentionchannel = relationship("RetentionChannel", backref='retentionchannel')

