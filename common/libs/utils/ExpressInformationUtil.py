# -*- coding:utf-8 -*-
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
        pass

        return ''
