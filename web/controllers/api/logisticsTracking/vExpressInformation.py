# -*- coding:utf-8 -*-

from web.controllers.api import api
from web.httpCode import APIResponse
from web.validators.api.ExpressInformationForm import GetDeliveryNodeForm
from common.libs.utils.ExpressInformationUtil import ExpressInformationServe


@api.route('/GetDeliveryNodeForm', methods=['POST', 'GET'])
def get_delivery_node():
    form = GetDeliveryNodeForm().validate_for_forms().to_dict()

    data = ExpressInformationServe.get_express_info(waybill_no=form['Waybill_No'], company=form['Waybill_Company'])

    resp = {
        'data': data
    }
    return APIResponse(data=resp)
