# -*- coding:utf-8 -*-
from web.validators import BaseForm
from wtforms import StringField
from wtforms.validators import DataRequired


class UserRegistrationForm(BaseForm):
    user_name = StringField(validators=[DataRequired('缺少用户名称')])
    password = StringField(validators=[DataRequired('缺少用户密码')])
    account = StringField(validators=[DataRequired('缺少用户账号')])
