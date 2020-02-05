# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/3
"""
from flask import current_app
from obs import ObsClient

__author__ = 'caijinxu'


class HWOBS:
    def __init__(self):
        self.obsclient = ObsClient(access_key_id=current_app.config.HW_ACCESS_KEY_ID,
                                   secret_access_key=current_app.config.HW_SECRET_ACCESS_KEY,
                                   server=current_app.config.HW_SERVER)

    def mv(self, srcbucketname, src_obj_key, destbucketname, dest_obj_key):
        """移动对象"""
        resp = self.obsclient.copyObject(srcbucketname, src_obj_key, destbucketname, dest_obj_key)
        if resp.status >= 300:
            raise Exception("OBS MV 复制对象出错 errorMessage:", resp.errorMessage, "errorCode:", resp.errorCode)
        else:
            res = self.obsclient.deleteObject(srcbucketname, src_obj_key)
            if res.status >= 300:
                raise Exception("OBS MV 删除源对象时出错 errorMessage:", res.errorMessage, "errorCode:", res.errorCode)
