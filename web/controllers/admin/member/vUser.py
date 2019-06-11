# -*- coding:utf-8 -*-
from web.controllers.admin import admin
from web.httpCode import APIResponse
from web.validators.admin.MemberForm import UserRegistrationForm, UserLoginForm, UserGetInfoForm
from common.models.admin.mMember import MemberModel
from common.libs.tools.Token import generate_token


@admin.route('/user/registered', methods=['POST'])
def user_registered():
    form = UserRegistrationForm().validate_for_forms().to_dict()
    member = MemberModel.create_member(user_name=form['user_name'], password=form['password'],
                                       account=form['account'])

    return APIResponse(data=member.to_dict())


@admin.route('/login', methods=['POST'])
def user_login():
    form = UserLoginForm().validate_for_forms().to_dict()

    token = generate_token(form['user_id'])

    data = {
        'token': token
    }
    return APIResponse(data=data)


@admin.route('/get_info', methods=['GET'])
def get_info():
    form = UserGetInfoForm().validate_for_forms().to_dict()

    info = {
        'name': 'super_admin',
        'user_id': '1',
        'access': ['super_admin', 'admin'],
        'token': form['token'],
        'avator': 'https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png'
    }

    return APIResponse(info)
