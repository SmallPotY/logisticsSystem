# -*- coding:utf-8 -*-
import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column
from contextlib import contextmanager
from web.httpCode.code import NotFound, DatabaseException
from sqlalchemy.sql import func


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            from application import app
            app.logger.error(e)
            db.session.rollback()
            raise DatabaseException()


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound('查无记录')
        return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound('查无记录')
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    revision = db.Column(db.SmallInteger, nullable=False, default="0", server_default="0", comment="乐观锁")
    status = Column(db.SmallInteger, nullable=False, default=1, server_default="1")
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, server_default=func.now())
    updated_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, server_default=func.now())
    created_by = db.Column(db.String(32), nullable=False, default="system", server_default="system")
    updated_by = db.Column(db.String(32), nullable=False, default="system", server_default="system")

    def __init__(self):

        pass

    def __getitem__(self, item):
        return getattr(self, item)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    @classmethod
    def u_(cls, **kwargs):
        """
        根据传入字典更新字段,需要id
        :param kwargs: 更新参数,需要传递id
        :return: 更新后的对象
        """
        with db.auto_commit():
            tmp = cls.query.get_or_404(kwargs.get('id', 0))
            for k, v in kwargs.items():
                if hasattr(tmp, k):
                    setattr(tmp, k, v)
            db.session.add(tmp)
        return tmp

    @classmethod
    def d_(cls, **kwargs):
        with db.auto_commit():
            tmp = cls.query.get_or_404(kwargs.get('id', 0))
            tmp.status = 0

    @classmethod
    def c_(cls, **kwargs):
        """
        新增一条记录
        :param kwargs: 字段参数
        :return: 新增对象
        """
        with db.auto_commit():
            tmp = cls()
            for k, v in kwargs.items():
                if hasattr(tmp, k):
                    setattr(tmp, k, v)
            db.session.add(tmp)
        return tmp
