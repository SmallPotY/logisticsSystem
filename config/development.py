# -*- coding:utf-8 -*-
from configparser import ConfigParser

config = ConfigParser()
config.read("secret.ini")

SERVER_PORT = 8889  # 端口号
SERVER_HOST = '127.0.0.1'  # 访问地址
DEBUG = True  # 调试模式
RELEASE_VERSION = '1.0'  # 发布版本

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = config.get('AliMySQL', 'USERNAME')
PASSWORD = config.get('AliMySQL', 'PASSWORD')
HOST = config.get('AliMySQL', 'HOST')
PORT = config.get('AliMySQL', 'PORT')
DATABASE = config.get('AliMySQL', 'DATABASE')
SQLALCHEMY_ENCODING = 'utf-8'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                          PORT, DATABASE)
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

DOMAIN = "http://{}:{}".format(SERVER_HOST, SERVER_PORT)


