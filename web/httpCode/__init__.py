# -*- coding:utf-8 -*-
from flask import request, json
from werkzeug.exceptions import HTTPException


class APIResponse(HTTPException):
    code = 200
    msg = 'Success'
    error_code = 0
    data = {}

    def __init__(self, msg=None, code=None, error_code=None, headers=None, data=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if headers:
            self.headers = headers
        if data:
            self.data = data
        super(APIResponse, self).__init__(msg, None)

    def get_body(self, environ=None):
        """
        定义api返回内容
        """
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param(),
            data=self.data,
            param=self.get_url_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]

    @staticmethod
    def get_url_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        if len(main_path) > 1:
            return main_path[1]
        return None


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None,
                 headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
