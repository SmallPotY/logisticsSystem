# -*- coding:utf-8 -*-
import xlrd
from jobs.Email.jobEmail import get_mail_attachment
from configparser import ConfigParser
from common.libs.utils.ExpressInformationUtil import ExpressInformationServe
from jobs.TimedTask.jobUpdateProgress import get_update_progress
from log import log_file_path
from common.libs.tools.Log import TNLog

timedTaskLog = TNLog('定时任务日志', log_file_path)

config = ConfigParser()
config.read("secret.ini")

emailHost = config.get('EmailKey', 'emailHost')
emailUser = config.get('EmailKey', 'emailUser')
emailPass = config.get('EmailKey', 'emailPass')


def request_aip(parameter):
    """获取快递信息更新"""
    data = ExpressInformationServe.get_express_info(waybill_no=parameter['Waybill_No'],
                                                    company=parameter['Waybill_Company'])
    data = ExpressInformationServe.unified_format(data=data, source=parameter['Waybill_Company'])

    order_time = parameter.get('order_time', '0000-00-00 00:00:00')
    to_address = parameter.get('to_address', 'default')
    from_address = parameter.get('from_address', 'default')
    identification = parameter.get('identification', 'default')
    ExpressInformationServe.save_to_redis(waybill_info=data, waybill_company=parameter['Waybill_Company'],
                                          waybill_no=parameter['Waybill_No'], action=parameter['action'],
                                          order_time=order_time,
                                          to_address=to_address, from_address=from_address,
                                          identification=identification, queue=parameter['queue'])


def job_import_mail_data(from_address, identification, key_word):
    """
    下载邮件, 并将邮件内数据发送至查询接口
    :param from_address: 默认发件地
    :param identification: 运单标识
    :param key_word: 邮件关键字
    :return:
    """
    timedTaskLog.info('执行=>job_import_mail_data')

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
        timedTaskLog.error(err)


def job_update_progress(interval):
    timedTaskLog.info('执行=>job_update_progress')

    item = get_update_progress(interval)

    for i in item:
        parameter = {
            'Waybill_Company': i[1],
            'Waybill_No': i[0],
            'access_id': 'yB6RXFSJNR',
            'secret_key': 'dd33jOzzy3',
            'dataStorage': 'action',
            'action': 'update',
            'queue': 'list'
        }
        request_aip(parameter)


c = 1


def job_check(s):
    global c
    c += s
    print(c)


class JobsConfig:
    JOBS = [
        {
            'id': 'importEmailData',
            'func': job_import_mail_data,
            'args': ('广东省', '肇庆唯品会', '预警编号5372：肇庆圆通出仓数据'),
            'trigger': 'cron',
            'hour': 1,
            'minute': 1
            # 'trigger': 'interval',
            # 'seconds': 5
        },
        {
            'id': 'job_update_progress',
            'func': job_update_progress,
            'args': (4,),
            # 'trigger': 'cron',
            # 'hour': 1,
            # 'minute': 1
            'trigger': 'interval',
            'minutes': 2
            # 'hours': 4
        },
        {
            'id': 'job_check',
            'func': job_check,
            'args': (1,),
            'trigger': 'interval',
            'seconds': 5
        },
    ]


if __name__ == '__main__':
    test = get_mail_attachment(email_host=emailHost, email_user=emailUser, email_pass=emailPass,
                               key_word='预警编号5372：肇庆圆通出仓数据')

    print(test)
