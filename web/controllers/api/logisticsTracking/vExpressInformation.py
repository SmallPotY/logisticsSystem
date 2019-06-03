# -*- coding:utf-8 -*-
import datetime
import json

from application import app
from web.controllers.api import api
from web.httpCode import APIResponse
from web.validators.api.ExpressInformationForm import GetDeliveryNodeForm
from common.libs.utils.ExpressInformationUtil import ExpressInformationServe


@api.route('/GetDeliveryNodeForm', methods=['POST'])
def get_delivery_node():
    form = GetDeliveryNodeForm().validate_for_forms().to_dict()

    data = ExpressInformationServe.get_express_info(waybill_no=form['Waybill_No'], company=form['Waybill_Company'])

    resp = {
        'data': ExpressInformationServe.unified_format(data=data, source=form['Waybill_Company'])
    }

    if form['dataStorage'] == 'action':
        save_to_redis(waybill_info=data, waybill_company=form['Waybill_Company'], waybill_no=form['Waybill_No'],
                      action=form['action'], order_time=form['order_time'], to_address=form['to_address'],
                      from_address=form['from_address'], identification=form['identification'], queue=form['queue'])

    return APIResponse(data=resp)


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
