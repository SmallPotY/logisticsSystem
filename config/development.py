# -*- coding:utf-8 -*-
from configparser import ConfigParser

config = ConfigParser()
config.read("secret.ini")

SERVER_PORT = 8889
SERVER_HOST = '127.0.0.1'
DEBUG = True
RELEASE_VERSION = '1.0'

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

# ---------------------redis配置----------------------------

REDIS_HOST = config.get('Redis', 'REDIS_HOST')
REDIS_PORT = config.get('Redis', 'REDIS_PORT')
REDIS_PARAMS = config.get('Redis', 'REDIS_PARAMS')
DB = config.get('Redis', 'DB')
REDIS_KEY = config.get('Redis', 'REDIS_KEY')
