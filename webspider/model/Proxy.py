# python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Proxy(Base):
    __tablename__ = 'Proxy'

    id = Column(Integer, primary_key=True)
    haship = Column(String(32))
    ip = Column(String(16))
    port = Column(Integer)
    create_time = Column(Integer)
