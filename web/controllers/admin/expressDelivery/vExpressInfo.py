# -*- coding:utf-8 -*-
from web.controllers.admin import admin
from web.httpCode import APIResponse
from web.validators.admin.ExpressForm import ReqExpressDataForm, ReqExpressHomeForm
from common.libs.utils.ExpressInfoUtils import ExpressInfoServer
from application import db


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


@admin.route('/home', methods=['POST'])
def express_home():
    req = ReqExpressHomeForm().validate_for_forms().to_dict()

    start_date, end_date = req['dateRang'] if req['dateRang'] else ['', '']
    company = req['company'] if req['company'] else ''

    express_status = visualization_express_status(start_date, end_date, company)
    to_address = visualization_to_address(start_date, end_date, company)
    express_progress = visualization_express_progress(start_date, end_date, company)
    process_use_time = visualization_process_use_time(start_date, end_date, company)
    logistics_stagnation = visualization_logistics_stagnation(start_date, end_date, company)
    data = {
        'express_status': express_status,
        'to_address': to_address,
        'express_progress': express_progress,
        'process_use_time': process_use_time,
        'logistics_stagnation': logistics_stagnation
    }

    return APIResponse(data=data)


def visualization_express_status(start_date, end_date, company):
    sql = "SELECT express_status, count(*) FROM EXPRESS_INFO WHERE 1=1"

    if start_date:
        sql += " AND order_time>='{start_date}' "
    if end_date:
        sql += " AND order_time<='{end_date}' "
    if company:
        sql += " AND express_company='{company}' "
    sql += " GROUP BY express_status"
    sql = sql.format(start_date=start_date, end_date=end_date, company=company)

    output = db.session.execute(sql)
    result = output.fetchall()

    express_status = []
    for i in result:
        tmp = {
            'value': i[1],
            'name': i[0]
        }
        express_status.append(tmp)
    return express_status


def visualization_to_address(start_date, end_date, company):
    sql = "SELECT to_address,COUNT(*) as total FROM EXPRESS_INFO WHERE 1=1"
    if start_date:
        sql += " AND order_time>='{start_date}' "
    if end_date:
        sql += " AND order_time<='{end_date}' "
    if company:
        sql += " AND express_company='{company}' "

    sql += " GROUP BY to_address ORDER BY total DESC limit 10"
    sql = sql.format(start_date=start_date, end_date=end_date, company=company)

    output = db.session.execute(sql)
    result = output.fetchall()

    to_address = []
    quantity = []
    for i in result:
        quantity.append(i[1])
        to_address.append(i[0])

    bar = {
        'key': to_address,
        'value': quantity
    }

    return bar


def visualization_express_progress(start_date, end_date, company):
    sql = "SELECT DATE_FORMAT(order_time,'%m-%d') days,express_status ,count(*) total FROM EXPRESS_INFO WHERE 1=1"
    if start_date:
        sql += " AND order_time>='{start_date}' "
    if end_date:
        sql += " AND order_time<='{end_date}' "
    if company:
        sql += " AND express_company='{company}' "

    sql += " GROUP BY days ,express_status ORDER BY days ,express_status "
    sql = sql.format(start_date=start_date, end_date=end_date, company=company)

    output = db.session.execute(sql)
    result = output.fetchall()

    all_types = {}
    data_list = []
    for i in result:
        _date, _type, _number = i
        if _date in data_list:

            if all_types.get(_type):
                all_types[_type].append(_number)
            else:
                all_types[_type] = [0] * len(data_list)
                all_types[_type][-1] = _number

        else:
            for k, v in all_types.items():
                if len(v) < len(data_list):
                    all_types[k].append(0)

            data_list.append(_date)
            if all_types.get(_type):
                all_types[_type].append(_number)
            else:
                all_types[_type] = [0] * len(data_list)
                all_types[_type][-1] = _number
    for k, v in all_types.items():
        if len(v) < len(data_list):
            all_types[k].append(0)

    ret = {
        'data_list': data_list,
        'all_types': all_types
    }
    return ret


def visualization_process_use_time(start_date, end_date, company):
    sql = """
        SELECT CASE WHEN TimeStampDiff(day,collection_time,NOW()) < 72 then '低于72/h'
        WHEN TimeStampDiff(day,collection_time,NOW()) between 72 and 120 then '72~120/h'
        WHEN TimeStampDiff(day,collection_time,NOW()) between 121 and 168 then '120~168/h'
        ELSE '>168' end as d,count(*) as number
        FROM EXPRESS_INFO WHERE express_status!='签收'
        """
    if start_date:
        sql += " AND order_time>='{start_date}' "
    if end_date:
        sql += " AND order_time<='{end_date}' "
    if company:
        sql += " AND express_company='{company}' "

    sql += """ group by
            case when TimeStampDiff(day,collection_time,NOW()) < 72 then '低于72/h'
            when TimeStampDiff(day,collection_time,NOW()) between 72 and 120 then '72~120/h'
            when TimeStampDiff(day,collection_time,NOW()) between 121 and 168 then '120~168/h'
            else '>168' end """
    sql = sql.format(start_date=start_date, end_date=end_date, company=company)

    output = db.session.execute(sql)
    result = output.fetchall()
    ret = []
    for i in result:
        ret.append({
            'key': i[0],
            'value': i[1]
        })
    return ret


def visualization_logistics_stagnation(start_date, end_date, company):
    sql = """
        SELECT CASE WHEN TimeStampDiff(day,latest_time,NOW()) < 72 then '低于72/h'
        WHEN TimeStampDiff(day,latest_time,NOW()) between 72 and 120 then '72~120/h'
        WHEN TimeStampDiff(day,latest_time,NOW()) between 121 and 168 then '120~168/h'
        ELSE '>168' end as d,count(*) as number
        FROM EXPRESS_INFO WHERE express_status!='签收'
        """
    if start_date:
        sql += " AND order_time>='{start_date}' "
    if end_date:
        sql += " AND order_time<='{end_date}' "
    if company:
        sql += " AND express_company='{company}' "

    sql += """ group by
            case when TimeStampDiff(day,latest_time,NOW()) < 72 then '低于72/h'
            when TimeStampDiff(day,latest_time,NOW()) between 72 and 120 then '72~120/h'
            when TimeStampDiff(day,latest_time,NOW()) between 121 and 168 then '120~168/h'
            else '>168' end """
    sql = sql.format(start_date=start_date, end_date=end_date, company=company)

    output = db.session.execute(sql)
    result = output.fetchall()
    ret = []
    for i in result:
        ret.append({
            'key': i[0],
            'value': i[1]
        })
    return ret
