# python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Page(Base):
    __tablename__ = 'Page'

    id = Column(Integer, primary_key=True)
    rule_id = Column(Integer)
    url = Column(String(500))
    urlmd5 = Column(String(32))
    site_name = Column(String(200))
    html_title = Column(String(500))
    save_path = Column(String(200))
    save_time = Column(Integer)
    title = Column(String(200))
    thumb = Column(String(500))
    img_list = Column(String(1000))
    body = Column(Text)
    publish_time = Column(String(30))
    source_site = Column(String(50))
    flag = Column(Boolean)
