# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/3
"""
from app.libs.hw_obs import HWOBS
from app.settings import OBS_BUCKET_URL
__author__ = 'caijinxu'


def recover_obs_file(recover_img_urls):
    """传入obs上对应域名链接bie列表,返回一个url是否恢复成功的字典"""
    obs = HWOBS()
    result = dict()
    for recover_img in recover_img_urls:
        result[recover_img] = False
        for url, buckets in OBS_BUCKET_URL:
            if url in recover_img:
                imgkey = recover_img.replace(url, '')
                try:
                    obs.mv(buckets[1], imgkey, buckets[0], imgkey)
                    result[recover_img] = True
                except Exception as e:
                    print(e)
    return result

