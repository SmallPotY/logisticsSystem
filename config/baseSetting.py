# -*- coding:utf-8 -*-

BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

SECRET_KEY = "O*eyUor#8vnWL2jgcGHi&gcdxP^j%PSoUOe^FMSTmWZJjVOYaGPT7Pj0vL1VB@vYfJS4X1W%"

JSON_AS_ASCII = False  # 让json显示中文

LOG_MAX_BYTES = 2097152  # 文件大小上限 Bytes
LOG_BACKUP_COUNT = 3  # 备份文件数
LOG_FILE_HANDLER = 'logging.DEBUG'  # 日志记录等级
LOG_STREAM_HANDLER = 'logging.DEBUG'  # 日志输出等级
LOG_FILE_FILENAME = "app.log"  # 日志明
LOG_FORMAT = "%(asctime)s [%(levelname)s] - %(message)s"  # 输出格式化
