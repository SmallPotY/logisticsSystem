# -*- coding:utf-8 -*-

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
        ExpressInformationServe.save_to_redis(waybill_info=data, waybill_company=form['Waybill_Company'],
                                              waybill_no=form['Waybill_No'],
                                              action=form['action'], order_time=form['order_time'],
                                              to_address=form['to_address'],
                                              from_address=form['from_address'], identification=form['identification'],
                                              queue=form['queue'])

    return APIResponse(data=resp)
