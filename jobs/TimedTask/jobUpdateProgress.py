# -*- coding:utf-8 -*-

from jobs.jobsDB import exec_sql_have_return


def get_update_progress(interval):
    """
    :param interval: 多长时间更新一次,单位小时
    :return:
    """

    sql = """
        SELECT express_no,express_company FROM `EXPRESS_INFO` WHERE has_end=0
        AND updated_time < date_sub(now(), interval {interval} hour)
    """.format(interval=interval)

    result = exec_sql_have_return(sql)

    ret = []
    for i in result:
        ret.append(i)

    return ret



