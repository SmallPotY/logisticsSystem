# -*- coding:utf-8 -*-
import datetime
import json
from common.libs.ExternalApi.ZTO import request_zto_api
from common.libs.ExternalApi.YTO import request_yto_api
from web.httpCode import APIException


branch = {
    'zto': request_zto_api,
    'yto': request_yto_api
}


class ExpressInformationServe:
    @staticmethod
    def get_express_info(company, waybill_no):
        """
        :param waybill_no: 快递单号
        :param company: 快递公司代码: zto,yto
        :return: 快递信息json
        """
        api = branch.get(company)

        if not api:
            err = '快递公司代码:{} 不存在!'.format(company)
            raise APIException(err)

        return api(waybill_no)

    @staticmethod
    def unified_format(data, source):
        """
        将外部接口获取到的数据进行整理,再进行统一返回
        :param source: 数据来源
        :param data: 数据内容
        :return:
        """
        if source in ['yto']:
            return data

        elif source in ['zto']:
            ret = []
            resp_data = data['data'][0]['traces']
            resp_bill_code = data['data'][0]['billCode']

            for i in resp_data:
                tmp = {
                    'ProcessInfo': i.get('desc', None),
                    'Upload_Time': i.get('scanDate', None),
                    'Waybill_No': resp_bill_code,
                }
                ret.append(tmp)
            if not ret:
                ret = {
                    "message": "该单号暂无物流进展",
                    "status": "0"
                }
            return ret

        raise APIException('快递代码错误')

    @staticmethod
    def save_to_redis(waybill_info, waybill_company, waybill_no, action, order_time, to_address, from_address,
                      identification, queue):
        """
        将信息暂存到redis中,等待入库

        :param queue: 当值为stack时,数据优先处理
        :param identification: 运单标识,仅action为create时生效
        :param from_address:  发件地,仅action为create时生效
        :param to_address: 目的地,仅action为create时生效
        :param order_time: 订单时间,仅action为create时生效
        :param waybill_info: 单号信息
        :param waybill_company: 快递公司代码
        :param waybill_no: 快递单号
        :param action: create:创建新记录; update(默认):更新原有记录
        """
        from application import app

        action = 'update' if action == 'update' else 'create'

        if action == 'create':
            store = {
                'to_address': to_address if to_address else 'default',
                'from_address': from_address if from_address else 'default',
                'identification': identification if identification else 'default',
                'order_time': order_time if order_time else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'data': waybill_info,
                'action': action,
                'express_no': waybill_no,
                'express_company': waybill_company
            }
        else:
            store = {
                'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'data': waybill_info,
                'action': action,
                'express_no': waybill_no,
                'express_company': waybill_company
            }

        if queue == 'stack':
            app.redis_store.lpush(app.config['REDIS_KEY'], json.dumps(store))
        else:
            app.redis_store.rpush(app.config['REDIS_KEY'], json.dumps(store))
