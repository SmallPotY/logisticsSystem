# -*- coding:utf-8 -*-
from common.models import Base, db


class ExpressCodeModel(Base):
    """-EXPRESS_MODULE-
        快递代码
    """
    __tablename__ = 'EXPRESS_CODE'

    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="id")
    express_company = db.Column(db.String(32), comment="快递公司")
    express_code = db.Column(db.String(32), comment="快递代码")
