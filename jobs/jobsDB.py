# -*- coding:utf-8 -*-

import pymysql
from DBUtils.PooledDB import PooledDB
import platform
from configparser import ConfigParser
from log import log_file_path
from common.libs.tools.Log import TNLog

timedTaskLog = TNLog('定时任务日志', log_file_path)


config = ConfigParser()
config.read("secret.ini")

env = platform.system()
if env == "Linux":
    user = config.get('AliMySQL', 'USERNAME')
    password = config.get('AliMySQL', 'PASSWORD')
    host = '127.0.0.1'
    db = config.get('AliMySQL', 'DATABASE')
    port = config.get('AliMySQL', 'PORT')
    set_session = ['SET AUTOCOMMIT = 1']
else:
    user = config.get('AliMySQL', 'USERNAME')
    password = config.get('AliMySQL', 'PASSWORD')
    host = config.get('AliMySQL', 'HOST')
    db = config.get('AliMySQL', 'DATABASE')
    port = config.get('AliMySQL', 'PORT')
    set_session = ['SET AUTOCOMMIT = 1']

pool = PooledDB(pymysql, 5, host=host, user=user, passwd=password, db=db, port=int(port), setsession=set_session)


def exec_sql_did_not_return(sql_string):
    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute(sql_string)
    except Exception as err:
        err = '{} => {}'.format(err, sql_string)
        timedTaskLog.error(err)
    finally:
        cur.close()
        conn.close()


def exec_sql_have_return(sql_string):
    conn = pool.connection()
    cur = conn.cursor()
    ret = []
    try:
        cur.execute(sql_string)
        ret = cur.fetchall()
    except Exception as err:
        err = '{} => {}'.format(err, sql_string)
        timedTaskLog.error(err)
        ret = []
    finally:
        cur.close()
        conn.close()
        return ret
