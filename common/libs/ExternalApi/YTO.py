# -*- coding:utf-8 -*-
import datetime
import hashlib
import requests
import json
from configparser import ConfigParser

config = ConfigParser()
config.read("secret.ini")

YTO_SECRET_KEY = config.get('ytoKey', 'secret_key')
YTO_USER_ID = config.get('ytoKey', 'user_id')
YTO_APP_KEY = config.get('ytoKey', 'app_key')


def get_sign(waybill_no):
    t = datetime.datetime.now().timetuple()
    timestamp = '{}-{}-{} {}:{}:{}'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

    secret_key = YTO_SECRET_KEY

    token = {
        'user_id': YTO_USER_ID,
        'app_key': YTO_APP_KEY,
        'format': 'JSON',
        'method': 'yto.Marketing.WaybillTrace',
        'timestamp': timestamp,
        'v': '1.01'
    }

    p = ['app_key', 'format', 'method', 'timestamp', 'user_id', 'v']
    sign = secret_key

    for i in p:
        sign += i + token[i]
    m = hashlib.md5()
    m.update(bytes(sign, 'ascii'))
    sign = m.hexdigest().upper()

    ret = {
        'sign': sign,
        'app_key': token['app_key'],
        'format': token['format'],
        'method': token['method'],
        'timestamp': token['timestamp'],
        'user_id': token['user_id'],
        'v': token['v'],
        'param': '[{"Number":"%s"}]' % waybill_no
    }

    return ret


def request_yto_api(waybill_no):
    data = get_sign(waybill_no)

    url = 'http://MarketingInterface.yto.net.cn'

    try:
        res = json.loads(requests.post(url=url, data=data).text)
    except Exception as err:
        print(err)
        res = {
            "message": '网络请求异常~',
            "status": "-1"
        }

    return res
