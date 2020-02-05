# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/5/6
"""
import json
from app.models.workerinfo import ConfigInfo
from app.models import db
from app.libs.etcd_handle import ETCD
from app.settings import ONLINKWORKER
__author__ = 'caijinxu'


def worker_choices():
    workerinfos = db.session.query(ConfigInfo.id, ConfigInfo.name).filter_by().all()
    return workerinfos


def worker_view(workers):
    """整理节点信息"""
    workerlist = []
    e = ETCD()
    for worker in workers:
        reginfo, kvdata = e.client.get(ONLINKWORKER + worker.workername)
        workerinfo = {
            'workername': worker.workername,
            'config_name': worker.config.name,
            'config_updatetime': worker.config.updatetime.strftime("%Y-%m-%d %H:%M:%S"),
            'config': worker.config.config,
            'remark': worker.remark
        }
        if reginfo:
            rinfo = json.loads(reginfo)
            workerinfo["worker_updatetime"] = rinfo["config_updatetime"]
            if workerinfo['config_updatetime'] == workerinfo["worker_updatetime"]:
                workerinfo['bg_status'] = "success"
                workerinfo["status"] = "正常"
            else:
                workerinfo['bg_status'] = "warning"
                workerinfo["status"] = "节点配置与服务器不一致，请重新下发配置"
        else:
            workerinfo['bg_status'] = "danger"
            workerinfo["worker_updatetime"] = ''
            workerinfo["status"] = "未找到节点，请检查节点是否正常工作"
        workerlist.append(workerinfo)
    return workerlist