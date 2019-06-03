# -*- coding:utf-8 -*-
from web.controllers.admin import admin
from web.httpCode import APIResponse
from web.validators.admin.MemberForm import UserRegistrationForm
from common.models.admin.mMember import MemberModel


@admin.route('/user/registered', methods=['POST'])
def user_registered():
    form = UserRegistrationForm().validate_for_forms().to_dict()
    member = MemberModel.create_member(user_name=form['user_name'], password=form['password'],
                                       account=form['account'])

    return APIResponse(data=member.to_dict())
