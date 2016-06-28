# python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Classify(Base):
    __tablename__ = 'classify'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    sort = Column(Integer)
