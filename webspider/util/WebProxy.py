# python
# -*- coding: utf-8 -*-
"""
主要是封装了代理的访问,切换,添加删除等操作
"""
import requests
import logging
from sqlalchemy import exc
import UserAgent as userAgent
from conf.config import DBSession, check_proxy_url
from model.Proxy import Proxy


def get_proxy_list():
    """ 获取代理列表"""
    db = DBSession()
    proxy_list = db.query(Proxy).all()
    db.close()
    return proxy_list


def get_proxy_url():
    """获取一个代理链接"""
    proxy_list = get_proxy_list()
    proxy_url = "http://%s:%s" % (proxy_list[0]['ip'], proxy_list[0]['port'])
    return proxy_url


# def create_proxy(timeout=3):
#     """
#     爬虫抓取代理
#     返回一个dict类型 timeout header 和proxy
#     返回前检查一下代理是否能用
#     不能用则删除并重新换一个代理
#     :param timeout: 超时时间
#     """
#     proxy_list = get_proxy_list()
#     proxy = choice(proxy_list)
#     if check_proxy(ip=proxy['ip'], port=proxy['port']):
#         request = {'proxies': proxy, 'header': get_user_agent(), 'timeout': timeout}
#         return request
#     else:
#         # 删除代理ip 且重新生成一个
#         delete_proxy(proxy['ip'], proxy['port'])
#         request = create_proxy(timeout)
#         return request


def get_user_agent():
    """ 获取头协议 """
    user_agent = {'User-Agent': userAgent.get_user_agent()}
    return user_agent


def check_proxy(ip, port):
    """ 检查代理是否正常
    :param ip: 代理IP
    :param port: 代理端口
    """
    proxy_check_url = check_proxy_url if check_proxy_url else 'http://www.baidu.com'

    proxy_url = "%s:%s" % (ip, port)
    proxies = {"http": proxy_url, }
    header = get_user_agent()
    try:
        req = requests.get(proxy_check_url, proxies=proxies, timeout=3, headers=header)
        if req.status_code == requests.codes.ok:
            return True
        else:
            return False
    except Exception, e:
        return False


def delete_proxy(ip, port):
    """ 删除数据库中的代理
    :param ip: ip
    :param port: 端口
    """
    if ip != "" and port != "":
        db = DBSession()
        db.query(Proxy).filter(Proxy.ip == ip).filter(Proxy.port == port).delete()
        try:
            db.commit()
            return True
        except exc.SQLAlchemyError, e:
            logging.info("Delete Proxy Error:", format(e))
            return False
