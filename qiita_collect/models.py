# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy import (Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)
from sqlalchemy.ext.declarative import declarative_base

CONNECTION_STRING = 'sqlite:///qiita_collect.db'
# CONNECTION_STRING = '{drivername}://{user}:{password}@{host}:{port}/{db_name}?charset=utf8'.format(
#     drivername = 'mysql+pymysql',
#     user = 'scrapy',
#     password = 'scrapy',
#     host = 'localhost',
#     port = '3306',
#     db_name = 'qiita_collect'
# )

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(CONNECTION_STRING, echo=True)

def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class QiitaCollectDatabase(DeclarativeBase):
    __tablename__ = 'qiita_posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(255))
    title = Column(String(255))
    url = Column(String(255))