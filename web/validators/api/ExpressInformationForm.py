# -*- coding:utf-8 -*-
from web.httpCode.code import ParameterException, AuthFailed
from web.validators import BaseForm
from wtforms import StringField
from wtforms.validators import DataRequired
from common.models.admin.mMember import MemberModel


class GetDeliveryNodeForm(BaseForm):
    access_id = StringField(validators=[DataRequired('缺少参数:access_id')])
    secret_key = StringField(validators=[DataRequired('缺少参数:secret_key')])
    Waybill_No = StringField(validators=[DataRequired('缺少参数:Waybill_No')])
    Waybill_Company = StringField(validators=[DataRequired('缺少参数:Waybill_Company')])

    dataStorage = StringField()
    action = StringField()
    order_time = StringField()
    to_address = StringField()
    from_address = StringField()
    identification = StringField()
    queue = StringField()

    def validate_for_forms(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)

        access = MemberModel.query.filter_by(access_id=self.access_id.data, secret_key=self.secret_key.data).first()
        if not access:
            raise AuthFailed('secret_key错误!')

        self.Waybill_Company.data = self.Waybill_Company.data.lower()

        return self
