#  python
# -*- coding: utf-8 -*-
# from sqlalchemy import exc
from conf.config import DBSession
from util import WebProxy as webProxy
from model.Proxy import Proxy

db = DBSession()
ips = db.query(Proxy).all()

for item in ips:
    ret = webProxy.check_proxy(item.ip, item.port)
    if not ret:
        webProxy.delete_proxy(item.ip, item.port)

