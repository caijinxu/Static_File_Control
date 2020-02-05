# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/22
"""
import datetime
from hashlib import sha1
import hmac
import base64
import requests
import json
from app.secure import CDNAPIKEY, CDNUSERNAME

__author__ = 'caijinxu'


def cdn_handle(updata):
    userName = CDNUSERNAME  # 替换成真实账号；Replace it with name you want to type
    apikey = CDNAPIKEY  # 替换成真实账号的apikey；Replace it with key you get
    accept = 'application/json'  # 填写返回接收数据模式； Typing the mode returned data
    api_url = "https://open.chinanetcenter.com/ccm/purge/ItemIdReceiver"
    date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signed_apikey = hmac.new(apikey.encode(), date.encode(), sha1).digest()
    signed_apikey = base64.b64encode(signed_apikey)

    headers = {
        'Date': date,
        'Accept': accept,
        'Content-type': accept,
        'Authorization': 'Basic ' + signed_apikey.decode()
    }

    r = requests.post(api_url, auth=(userName, signed_apikey.decode()), headers=headers, data=json.dumps(updata))
    result = r.text
    return result

