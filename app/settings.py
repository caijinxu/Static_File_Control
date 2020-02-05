# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/3
"""

__author__ = 'caijinxu'



# 性能测试的阀值
DATABASE_QUERY_TIMEOUT = 0.5

SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_CHECK_DEFAULT = False

SQLALCHEMY_ECHO = True

# obs 域名对应bucket和存放删除对象的bucket
OBS_BUCKET_URL = {
    "http://test.test.com/": ["test.test.com", "test.test.com-delete"]
}



HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86'
                         ' Safari/537.36',
           }

BABEL_DEFAULT_LOCALE = 'zh_CN'


# ETCD 目录设置
CONFIG_DIR = "/worker_config/"  # 下发worker节点配置信息，ETCD中目录
ONLINKWORKER = "/online_work/"  # 节点注册目录
RECOERTASK = "/services/recoerjob/"  # 恢复任务目录
DELETETASK = "/services/deletejob/"  # 删除任务目录
DEADLINKSDIR = "/deadlinks/"  # 死链处理目录

