# -*- coding: utf-8 -*-
import os
import time
import logging
import inspect
from logging.handlers import RotatingFileHandler


class TNLog:

    def create_handlers(self):
        log_levels = self.handlers.keys()

        for level in log_levels:
            path = os.path.abspath(self.handlers[level])
            self.handlers[level] = RotatingFileHandler(path, maxBytes=2097152, backupCount=4, encoding='utf-8')

    @staticmethod
    def print_now():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def __init__(self, log_name, save_path=None):
        """
        :param log_name: 日记名称
        :param save_path: 存储路径,默认当前路径
        """
        save_path = save_path if save_path else os.path.dirname(__file__)
        file_path = save_path + os.sep + log_name + os.sep
        if not os.path.exists(file_path):
            os.makedirs(file_path, 777)
        self.handlers = {
            logging.NOTSET: file_path + 'notset_%s.log' % log_name,
            logging.DEBUG: file_path + 'debug_%s.log' % log_name,
            logging.INFO: file_path + 'info_%s.log' % log_name,
            logging.WARNING: file_path + 'warning_%s.log' % log_name,
            logging.ERROR: file_path + 'error_%s.log' % log_name,
            logging.CRITICAL: file_path + 'critical_%s.log' % log_name
        }
        self.create_handlers()
        self.__loggers = {}

        log_levels = self.handlers.keys()

        for level in log_levels:
            logger = logging.getLogger(str(level))
            logger.addHandler(self.handlers[level])
            logger.setLevel(level)

            self.__loggers.update({level: logger})

    def get_log_message(self, level, message):
        frame, filename, line_no, function_name, code, un_know_field = inspect.stack()[2]

        '''日志格式：[时间] [类型] [记录代码] 信息'''

        return "[%s] [%s] [%s - %s - %s] %s" % (self.print_now(), level, filename, line_no, function_name, message)

    def info(self, message):
        message = self.get_log_message("info", message)
        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.get_log_message("error", message)
        self.__loggers[logging.ERROR].error(message)

    def warning(self, message):
        message = self.get_log_message("warning", message)
        self.__loggers[logging.WARNING].warning(message)

    def debug(self, message):
        message = self.get_log_message("debug", message)
        self.__loggers[logging.DEBUG].debug(message)

    def critical(self, message):
        message = self.get_log_message("critical", message)
        self.__loggers[logging.CRITICAL].critical(message)


if __name__ == "__main__":
    path = os.path.dirname(__file__)
    log = TNLog('日志测试', path)
    log.info('hhhhhhh')
