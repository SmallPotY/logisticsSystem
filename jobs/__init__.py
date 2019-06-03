# -*- coding:utf-8 -*-
import xlrd
from jobs.Email.jobEmail import get_mail_attachment
from configparser import ConfigParser

config = ConfigParser()
config.read("secret.ini")

emailHost = config.get('EmailKey', 'emailHost')
emailUser = config.get('EmailKey', 'emailUser')
emailPass = config.get('EmailKey', 'emailPass')


def job_import_mail_data(from_address, identification, key_word):
    ret = get_mail_attachment(email_host=emailHost, email_user=emailUser, email_pass=emailPass,
                              key_word=key_word)

    if ret[0]:
        path = ret[1]

        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)
        max_row = sheet.nrows
        for i in range(1, max_row):
            tmp = {
                'to_address': sheet.row_values(i)[4],
                'from_address': from_address,
                'identification': identification,
                'order_time': sheet.row_values(i)[0],
                'Waybill_Company': 'yto',
                'Waybill_No': sheet.row_values(i)[2],
                'access_id': 'yB6RXFSJNR',
                'secret_key': 'dd33jOzzy3',
                'dataStorage': 'action',
                'action': 'create'
            }
            print(tmp)
    else:
        err = ret[1]
        print(err)


class JobsConfig:
    JOBS = [
        {
            'id': 'job1',
            'func': job_import_mail_data,
            'args': ('广东省', '肇庆唯品会', '预警编号5372：肇庆圆通出仓数据'),
            # 'trigger': 'cron',
            # 'hour': 17,
            # 'minute': 8
            'trigger': 'interval',
            'seconds': 5

        }
    ]


if __name__ == '__main__':
    test = get_mail_attachment(email_host=emailHost, email_user=emailUser, email_pass=emailPass,
                               key_word='预警编号5372：肇庆圆通出仓数据')

    print(test)
