# -*- coding:utf-8 -*-
from flask import request
from wtforms import Form
from web.httpCode.code import ParameterException


class BaseForm(Form):

    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_forms(self):
        valid = super(BaseForm, self).validate()

        if not valid:
            raise ParameterException(msg=self.errors)
        return self

    def to_dict(self):
        """
        将验证后的信息转成字典
        :return:
        """
        fields = vars(self)['_fields']
        tmp = {}
        for i, j in fields.items():
            tmp[i] = j.data
        return tmp
