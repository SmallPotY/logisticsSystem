# -*- coding:utf-8 -*-
from web.controllers.admin import admin
from web.httpCode import APIResponse
from web.validators.admin.ExpressForm import ReqExpressDataForm
from common.libs.utils.ExpressInfoUtils import ExpressInfoServer


@admin.route('/reqExpressData', methods=['POST'])
def req_express_data():
    req = ReqExpressDataForm().validate_for_forms().to_dict()

    data, page = ExpressInfoServer.get_express_info(page_current=req['page_current'], page_size=req['page_size'],
                                                    date_rang=req['dateRang'], company=req['company'],
                                                    word_key=req['wordKey'])

    data = {
        'tableData': data,
        'page': page
    }
    return APIResponse(data=data)
