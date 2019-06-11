# -*- coding:utf-8 -*-
from web.httpCode.code import ParameterException, AuthFailed
from web.validators import BaseForm
from wtforms import StringField
from wtforms.validators import DataRequired
from common.models.admin.mMember import MemberModel


class UserRegistrationForm(BaseForm):
    user_name = StringField(validators=[DataRequired('缺少用户名称')])
    password = StringField(validators=[DataRequired('缺少用户密码')])
    account = StringField(validators=[DataRequired('缺少用户账号')])


class UserLoginForm(BaseForm):
    userName = StringField(validators=[DataRequired('请输入用户名')])
    password = StringField(validators=[DataRequired('请输入用密码')])
    user_role = StringField()
    user_id = StringField()

    def validate_for_forms(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)

        account = self.userName.data
        password = self.password.data

        member = MemberModel.query.filter_by(account=account).first()
        if not member:
            raise AuthFailed('账号不存在!')
        if not member.verify_password(password):
            raise AuthFailed('密码错误!')

        self.user_role.data = member.user_role
        self.user_id.data = member.id
        return self


class UserGetInfoForm(BaseForm):
    token = StringField(validators=[DataRequired('缺少token')])