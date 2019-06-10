# -*- coding:utf-8 -*-
from common.models.express.mExpressInfo import ExpressInfoModel
from sqlalchemy import extract, and_, or_


class ExpressInfoServer:

    @staticmethod
    def get_express_info(page_current, page_size, date_rang, company, word_key):
        query = ExpressInfoModel.query

        if date_rang:
            query = query.filter(ExpressInfoModel.order_time.between(date_rang[0], date_rang[1]))
        if word_key:
            query = query.filter(or_(
                ExpressInfoModel.express_no.ilike('%{}%'.format(word_key)),
                ExpressInfoModel.from_address.ilike('%{}%'.format(word_key)),
                ExpressInfoModel.to_address.ilike('%{}%'.format(word_key)),
                ExpressInfoModel.identification.ilike('%{}%'.format(word_key)),
            ))
        if company:
            query = query.filter(ExpressInfoModel.express_company.in_(company))

        data = query.limit(page_size).offset((page_current - 1) * page_size).all()

        ret = []
        for i in data:
            ret.append(i.to_dict())
        total = len(ret)

        page = {
            'current': page_current,
            'total': total,
            'page_size': page_size
        }
        return ret, page
