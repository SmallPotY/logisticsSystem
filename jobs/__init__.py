# -*- coding:utf-8 -*-
import xlrd
from jobs.Email.jobEmail import get_mail_attachment
from configparser import ConfigParser
from common.libs.utils.ExpressInformationUtil import ExpressInformationServe

config = ConfigParser()
config.read("secret.ini")

emailHost = config.get('EmailKey', 'emailHost')
emailUser = config.get('EmailKey', 'emailUser')
emailPass = config.get('EmailKey', 'emailPass')


def request_aip(parameter):
    data = ExpressInformationServe.get_express_info(waybill_no=parameter['Waybill_No'],
                                                    company=parameter['Waybill_Company'])
    data = ExpressInformationServe.unified_format(data=data, source=parameter['Waybill_Company'])

    ExpressInformationServe.save_to_redis(waybill_info=data, waybill_company=parameter['Waybill_Company'],
                                          waybill_no=parameter['Waybill_No'],
                                          action=parameter['action'], order_time=parameter['order_time'],
                                          to_address=parameter['to_address'],
                                          from_address=parameter['from_address'],
                                          identification=parameter['identification'],
                                          queue=parameter['queue'])


def job_import_mail_data(from_address, identification, key_word):
    """
    下载邮件, 并将邮件内数据发送至查询接口
    :param from_address: 默认发件地
    :param identification: 运单标识
    :param key_word: 邮件关键字
    :return:
    """
    ret = get_mail_attachment(email_host=emailHost, email_user=emailUser, email_pass=emailPass,
                              key_word=key_word)

    if ret[0]:
        path = ret[1]

        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)
        max_row = sheet.nrows
        for i in range(1, max_row):
            parameter = {
                'to_address': sheet.row_values(i)[4],
                'from_address': from_address,
                'identification': identification,
                'order_time': sheet.row_values(i)[0],
                'Waybill_Company': 'yto',
                'Waybill_No': sheet.row_values(i)[2],
                'access_id': 'yB6RXFSJNR',
                'secret_key': 'dd33jOzzy3',
                'dataStorage': 'action',
                'action': 'create',
                'queue': 'list'
            }
            request_aip(parameter)
    else:
        err = ret[1]
        print(err)


class JobsConfig:
    JOBS = [
        {
            'id': 'job1',
            'func': job_import_mail_data,
            'args': ('广东省', '肇庆唯品会', '预警编号5372：肇庆圆通出仓数据'),
            'trigger': 'cron',
            'hour': 1,
            'minute': 1
            # 'trigger': 'interval',
            # 'seconds': 5

        }
    ]


if __name__ == '__main__':
    test = get_mail_attachment(email_host=emailHost, email_user=emailUser, email_pass=emailPass,
                               key_word='预警编号5372：肇庆圆通出仓数据')

    print(test)
