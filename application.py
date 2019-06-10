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
            # 读取生产环境配置
            self.config.from_object('config.production')
        else:
            # 读取开发环境配置
            self.config.from_object('config.development')

        # 创建链接到redis数据库的对象
        global redis_store
        self.redis_store = redis.StrictRedis(host=self.config['REDIS_HOST'], port=self.config['REDIS_PORT'],
                                             password=self.config['REDIS_PARAMS'], db=self.config['DB'])
        db.init_app(self)
        self.config.from_object(JobsConfig())

        if env == "Linux":
            # linux下可以使用文件独享锁让定时任务只启动一次
            import atexit
            import fcntl
            f = open("scheduler.lock", "wb")
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                scheduler = APScheduler()
                scheduler.init_app(self)
                scheduler.start()
                print('启动定时任务')
            except Exception:
                pass
                print('仅存在一次定时任务,当前已存在一个')
            def unlock():
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()

            atexit.register(unlock)
        else:

            scheduler = APScheduler()
            scheduler.init_app(self)
            scheduler.start()


def create_models(application):
    with application.app_context():
        db.create_all()


APP_ROOT_PATH = os.path.dirname(__file__)
app = Application(__name__, template_folder=APP_ROOT_PATH + '/web/templates/',
                  static_folder=APP_ROOT_PATH + '/web/static',
                  root_path=APP_ROOT_PATH)

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
