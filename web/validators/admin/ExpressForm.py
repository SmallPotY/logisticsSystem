# -*- coding:utf-8 -*-
from web.httpCode.code import ParameterException
from web.validators import BaseForm
from wtforms import StringField
from common.libs.tools.DateTimeTools import DateTimeTools


class ReqExpressDataForm(BaseForm):
    page_current = StringField()
    page_size = StringField()

    dateRang = StringField()
    company = StringField()
    wordKey = StringField()

    def validate_for_forms(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)

        if not self.page_current.data:
            self.page_current.data = 1

        if not self.page_size.data:
            self.page_size.data = 40

        if self.dateRang.data:
            try:
                DateTimeTools.string_conversion_date(self.dateRang.data[0])
                DateTimeTools.string_conversion_date(self.dateRang.data[1])
            except Exception as err:
                self.dateRang.data = None
                del err
        return self
