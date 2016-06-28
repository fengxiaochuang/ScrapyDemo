# python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Rule(Base):
    __tablename__ = 'Rule'

    rule_id = Column(Integer, primary_key=True)
    weburl_id = Column(Integer)
    name = Column(String)
    allow_domains = Column(String)
    start_urls = Column(String)
    next_page = Column(String)
    extract_from = Column(String)
    allow_url = Column(String)
    title_xpath = Column(String)
    thumb_img_xpath = Column(String)
    body_xpath = Column(String)
    publish_time_xpath = Column(String)
    source_site_xpath = Column(String)
    enable = Column(Boolean)
