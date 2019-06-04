from flask import Flask, json
from werkzeug.exceptions import HTTPException
import platform
from common.models import db
from decimal import Decimal
import datetime
from logging.handlers import RotatingFileHandler
import logging
import os
from flask_cors import CORS
from web.httpCode import APIException
import redis
from jobs import JobsConfig

from flask_apscheduler import APScheduler

redis_store = None


class JSONEncoder(json.JSONEncoder):
    """JSON序列化一波"""

    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, set):
            return list(o)

        return json.JSONEncoder.default(self, o)


def create_log(application):
    """运行日志"""
    file_handler = RotatingFileHandler(application.config['LOG_FILE_FILENAME'],
                                       maxBytes=application.config['LOG_MAX_BYTES'],
                                       backupCount=application.config['LOG_BACKUP_COUNT'],
                                       encoding="UTF-8")
    stream_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(application.config["LOG_FORMAT"])
    file_handler.setLevel(eval(application.config['LOG_FILE_HANDLER']))
    file_handler.setFormatter(log_formatter)
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(eval(application.config['LOG_STREAM_HANDLER']))
    application.logger.addHandler(stream_handler)
    application.logger.addHandler(file_handler)
    application.logger.setLevel(logging.DEBUG)


class Application(Flask):
    json_encoder = JSONEncoder

    def __init__(self, import_name, template_folder=None, root_path=None, static_folder=None):
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=static_folder, )
        self.config.from_object('config.baseSetting')
        env = platform.system()
        if env == "Linux":
            print('**读取生产环境配置**')
            self.config.from_object('config.production')
        else:
            print('**读取开发环境配置**')
            self.config.from_object('config.development')
        db.init_app(self)

        # 创建链接到redis数据库的对象
        global redis_store
        self.redis_store = redis.StrictRedis(host=self.config['REDIS_HOST'], port=self.config['REDIS_PORT'],
                                             password=self.config['REDIS_PARAMS'], db=self.config['DB'])

        self.config.from_object(JobsConfig())

        scheduler = APScheduler()
        scheduler.init_app(self)
        scheduler.start()


def create_models(application):
    with application.app_context():
        db.create_all()


root_path = os.path.dirname(__file__)
app = Application(__name__, template_folder=root_path + '/web/templates/',
                  static_folder=root_path + '/web/static',
                  root_path=root_path)
create_log(app)
CORS(app, supports_credentials=True)


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, HTTPException):
        """可预知的错误"""
        code = e.code
        msg = e.description
        error_code = 999
        return APIException(msg, code, error_code)
    else:
        """不可预知的错误"""
        from flask import request
        url = request.url
        msg = "{} - {}".format(e, url)
        app.logger.error(msg)
        raise e
