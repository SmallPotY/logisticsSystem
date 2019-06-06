import logging
import os
from log import log_file_path

log_level = {
    'NOTSET': logging.NOTSET,
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


class SystemLog:
    def __init__(self, logger_name, file_path=None, levels=None):
        # 创建一个logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_path = file_path if file_path else log_file_path
        file_path = file_path + os.sep + logger_name
        if not os.path.exists(file_path):
            os.makedirs(file_path, 777)

        levels = levels if levels else ['INFO', 'WARNING', 'ERROR']
        for level in levels:
            log_info = log_level.get(level)
            if log_info:
                log_path = file_path + os.sep + logger_name + '_' + level + '.log'
                log = logging.FileHandler(log_path, encoding='utf-8')
                log.setLevel(log_info)
                log.filter(record=1)
                log.setFormatter(formatter)
                self.logger.addHandler(log)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger
