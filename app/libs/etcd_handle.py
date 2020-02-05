# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/8
"""
import etcd3
import json
import uuid
from app.secure import ETCDHOST, ETCDPORT, ETCDUSER, ETCDPASSWD
from app.settings import ONLINKWORKER, RECOERTASK, DELETETASK
__author__ = 'caijinxu'


class ETCD:
    def __init__(self):
        self.client = etcd3.Etcd3Client(host=ETCDHOST, port=ETCDPORT, user=ETCDUSER, password=ETCDPASSWD)

    def get_online_recover_worker(self):
        # 获取在线的worker节点

        etcdread = self.client.get_prefix(ONLINKWORKER)
        if etcdread:
            result = dict()
            for kvalue, kmatedata in etcdread:
                # rekey = chi["key"].replace("/online_work/", '')
                rekey = kmatedata.key.decode().replace(ONLINKWORKER, '')
                chivalue = json.loads(kvalue.decode())
                result[rekey] = chivalue
            return result
        else:
            return []

    def get_online_worker(self):
        # 获取在线的worker节点名和替换规则

        etcdread = self.client.get_prefix(ONLINKWORKER)
        if etcdread:
            result = dict()
            for kvalue, kmatedata in etcdread:
                # rekey = chi["key"].replace("/online_work/", '')
                rekey = kmatedata.key.decode().replace(ONLINKWORKER, '')
                kv = json.loads(kvalue.decode())
                chivalue = kv['config']
                result[rekey] = chivalue
            return result
        else:
            return []

    def send_url_ectd(self, urllist, handlemod, taskuuid):
        for url in urllist:
            task = {
                "taskuuid": taskuuid,
                "url": url.replace('\n', '').replace('\r', '').replace(' ', '')
            }
            if handlemod == 1:
                writekey = RECOERTASK + str(uuid.uuid4())
            else:
                writekey = DELETETASK + str(uuid.uuid4())
            lease = self.client.lease(60)
            self.client.put(writekey, json.dumps(task), lease)



if __name__ == '__main__':
    e = ETCD()
    onwork = e.get_online_worker()
    print(onwork)
    # # print(onwork._children)
    # # print(onwork._children)
    # e.client.
