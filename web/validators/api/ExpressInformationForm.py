# -*- coding:utf-8 -*-
from web.validators import BaseForm
from wtforms import StringField
from wtforms.validators import DataRequired


class GetDeliveryNodeForm(BaseForm):
    access_id = StringField(validators=[DataRequired('缺少参数:access_id')])
    secret_key = StringField(validators=[DataRequired('缺少参数:secret_key')])
    Waybill_No = StringField(validators=[DataRequired('缺少参数:Waybill_No')])
    Waybill_Company = StringField(validators=[DataRequired('缺少参数:Waybill_Company')])
