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
from datetime import datetime
from flask import request
from flask_xxl.apps.auth.models import User

class ConnectionRecord(Model):
    # keep track of people connecting
    ip_address = Column(String(15),nullable=False)
    date = Column(Date,default=datetime.now)

    def __init__(self):
        self.ip_address = request.remote_addr
        self.session.add(self)
        self.session.commit()

visitor_count = lambda: ConnectionRecord.query.count()

class ConnectionDict(object):
    pass

class Server(Model):
    __tablename__ = 'servers'
    __table_args__ = (
        UniqueConstraint('name','ip_address'),
    )
    
    accounts = relationship('Account',backref=backref(
            'server'),lazy='dynamic',cascade='all,delete-orphan')

    ip_address = Column(String(20),nullable=False,unique=True)
    name = Column(String(255),unique=True)
    connection_type = relationship('ConnectionType')
    connection_type_id = Column(Integer,ForeignKey('connection_types.id'))

    def __unicode__(self):
        return '{} @ {}'.format(self.name,self.ip_address)


class Account(Model):

    username = Column(String(255),nullable=False)
    password = Column(String(255),nullable=False)
    server_id = Column(Integer,ForeignKey('servers.id'))
    base_dir = Column(String(255),nullable=False)
    last_login = Column(Date)

    def __unicode__(self):
        return '{}'.format(self.username)#,self.server.name)


class ConnectionType(Model):

    name = Column(String(255),unique=True,nullable=False)
    connection_class = Column(String(255),nullable=False)

    def __unicode__(self):
        return self.name


class UserProfile(Model):
    
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('User',backref=backref(
        'profile',uselist=False),single_parent=True,cascade='all,delete-orphan')

    age = Column(Integer)
    date_added = Column(DateTime,default=datetime.now)
    description = Column(Text)

