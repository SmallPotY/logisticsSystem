# -*- coding:utf-8 -*-
from common.models import Base, db


class ExpressInfoModel(Base):
    """-EXPRESS_MODULE-
        快递信息
    """
    __tablename__ = 'EXPRESS_INFO'

    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="id")
    express_no = db.Column(db.String(32), comment="快递单号")
    express_company = db.Column(db.String(32), comment="快递公司")
    express_status = db.Column(db.String(32), comment="快递状态")
    collection_time = db.Column(db.DateTime, comment="揽收时间")
    latest_content = db.Column(db.String(512), comment="最新信息")
    latest_time = db.Column(db.DateTime, comment="最新时间")
    order_time = db.Column(db.DateTime, comment="订单日期")
    to_address = db.Column(db.String(32), comment="目的地")
    from_address = db.Column(db.String(32), comment="发件地")
    has_end = db.Column(db.SmallInteger, comment="是否完结")
    remarks = db.Column(db.String(3072), comment="备注信息")
