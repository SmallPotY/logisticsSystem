# -*- coding:utf-8 -*-
from common.models import Base, db
from passlib.apps import custom_app_context as pwd_context
from common.libs.tools.StringTools import StringTools
from web.httpCode.code import RepeatError


class MemberModel(Base):
    """-MEMBER-
        成员表
    """
    __tablename__ = 'MEMBER'

    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="id")
    user_name = db.Column(db.String(128), comment="用户名")
    account = db.Column(db.String(128), comment="账号")
    password_hash = db.Column(db.String(512), comment="密码")
    access_id = db.Column(db.String(128), comment="访问id")
    secret_key = db.Column(db.String(128), comment="访问秘钥")
    salt = db.Column(db.String(128), comment="加密盐")
    user_role = db.Column(db.String(64), comment="角色")
    enable_whitelist = db.Column(db.SmallInteger, comment="启用白名单")
    whitelist_address = db.Column(db.String(3072), comment="白名单授权地址")

    def hash_password(self, password):
        """
        hash加密
        """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """
        验证密码
        """
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    def create_member(user_name, password, account):
        """
        创建一个新账号
        """
        check_account = MemberModel.query.filter_by(account=account).first()
        if check_account:
            raise RepeatError('账号已存在!')
        while True:
            access_id = StringTools.get_random_string(10)
            not_repeating = MemberModel.query.filter_by(access_id=access_id).first()
            if not not_repeating:
                break
        with db.auto_commit():
            member = MemberModel()
            member.hash_password(password)
            member.account = account
            member.user_name = user_name
            member.access_id = access_id
            member.secret_key = StringTools.get_random_string(10)
            member.salt = StringTools.get_random_string(16)
            member.whitelist_address = '[]'
            member.enable_whitelist = 0
            member.user_role = 'default'
            db.session.add(member)
        return member
