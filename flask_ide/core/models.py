# -*- coding: utf-8 -*-

"""
    core blueprint for flask-cms
"""

from sqlalchemy.ext.declarative import declared_attr,declarative_base
from sqlalchemy import UniqueConstraint,Column,Integer,Text,String,Date,DateTime,ForeignKey,func,create_engine
from sqlalchemy.orm import backref, relationship,sessionmaker, scoped_session
from LoginUtils import encrypt_password as generate_password_hash
from LoginUtils import check_password as check_password_hash
import sys
import os
from flask_xxl.basemodels import BaseMixin as Model 


class ConnectionDict(object):
    pass

class Server(Model):
    __tablename__ = 'servers'
    __table_args__ = (
        UniqueConstraint('name','ip_address'),
        dict(extend_existing=True),
    )
    
    accounts = relationship('Account',backref=backref(
            'server',uselist=False),lazy='dynamic')

    ip_address = Column(String(20),nullable=False,unique=True)
    name = Column(String(255),unique=True)
    connection_type = relationship('ConnectionType')
    connection_type_id = Column(Integer,ForeignKey('connection_types.id'))

    def __unicode__(self):
        return '{} @ {}'.format(self.name,self.ip_address)


class Account(Model):
    __table_args__ = (
        dict(extend_existing=True),
    )

    username = Column(String(255),nullable=False)
    password = Column(String(255),nullable=False)
    server_id = Column(Integer,ForeignKey('servers.id'))
    base_dir = Column(String(255),nullable=False)
    last_login = Column(Date)
    server_id = Column(Integer,ForeignKey('servers.id'))

    def __unicode__(self):
        return '{}'.format(self.username)#,self.server.name)


class ConnectionType(Model):
    __table_args__ = (
        dict(extend_existing=True),
    )

    name = Column(String(255),unique=True,nullable=False)
    connection_class = Column(String(255),nullable=False)

    def __unicode__(self):
        return self.name


