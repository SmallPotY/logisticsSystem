# -*- coding:utf-8 -*-
import hashlib
import base64
import json
import requests

from configparser import ConfigParser

config = ConfigParser()
config.read("secret.ini")

ZTO_COMPANY_ID = config.get('ztoKey', 'company_id')
ZTO_DIGEST_KEY = config.get('ztoKey', 'digest_key')


def request_zto_api(waybill_no):
    company_id = ZTO_COMPANY_ID
    digest_key = ZTO_DIGEST_KEY
    url = 'http://japi.zto.cn/traceInterfaceNewTraces'

    post_fields = {'company_id': company_id, 'data': '["{}"]'.format(waybill_no), 'msg_type': 'NEW_TRACES'}

    str_to_digest = ''
    for key, value in post_fields.items():
        str_to_digest += (key + '=' + value + '&')
    str_to_digest = str_to_digest[:-1] + digest_key

    m = hashlib.md5()
    m.update(str_to_digest.encode("UTF-8"))

    data_digest = base64.b64encode(m.digest())

    headers = {
        'x-companyid': company_id,
        'x-datadigest': data_digest
    }

    res = json.loads(requests.post(url=url, data=post_fields, headers=headers).text)

    return res
