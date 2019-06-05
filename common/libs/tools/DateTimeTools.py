# -*- coding:utf-8 -*-
import datetime

from web.httpCode.code import ParameterException


class DateTimeTools:

    @staticmethod
    def string_conversion_date(s, datetime_format="%Y-%m-%d %H:%M:%S"):
        """
        字符串转成时间格式
        :param datetime_format: 字符串格式
        :param s: 内容为日期时间的字符串
        :return:
        """
        try:
            ret = datetime.datetime.strptime(s, datetime_format)
        except Exception as err:
            err = "字符串{s}转换日期or时间格式失败,{err}".format(s=s, err=err)
            raise ParameterException(err)
        return ret
