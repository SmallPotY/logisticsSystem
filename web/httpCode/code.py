# -*- coding:utf-8 -*-
from web.httpCode import APIResponse


class Success(APIResponse):
    code = 200
    msg = 'success'
    error_code = 0


class NotAllowed(APIResponse):
    code = 406
    msg = "不被允许的操作"
    error_code = 1000


class DeleteSuccess(Success):
    code = 202
    error_code = -1


class ServerError(APIResponse):
    code = 500
    msg = '未知的异常'
    error_code = 999


class RepeatError(APIResponse):
    code = 400
    msg = "存在相同记录"
    error_code = 1003


class DatabaseException(APIResponse):
    code = 500
    msg = '数据库异常'
    error_code = 999


class ClientTypeError(APIResponse):
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIResponse):
    code = 400
    msg = 'invalid parameter'
    error_code = 1002


class NotFound(APIResponse):
    code = 404
    msg = "the resource are not found..."
    error_code = 1001


class AuthFailed(APIResponse):
    code = 401
    error_code = 1005
    msg = 'authorization failed'


class Forbidden(APIResponse):
    code = 403
    error_code = 1004
    msg = 'Forbidden, not in scope'
