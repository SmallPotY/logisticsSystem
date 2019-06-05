# -*- coding:utf-8 -*-
from web.controllers.admin import admin
from web.httpCode import APIResponse
from web.validators.admin.ExpressForm import ReqExpressDataForm


@admin.route('/reqExpressData', methods=['POST'])
def req_express_data():
    req = ReqExpressDataForm().validate_for_forms().to_dict()



    return APIResponse()
