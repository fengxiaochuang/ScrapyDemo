# python
# -*- coding: utf-8 -*-
import sys
# import logging
from random import choice
from util.UserAgent import get_user_agent
from util import WebProxy as webProxy
from conf.config import confRedis
from scrapy.exceptions import IgnoreRequest
# from scrapy.http import XmlResponse
# import re
# import urlparse
# from pprint import pprint
# import gzip
# from scrapy.utils import gz


class SetProxyMiddleware(object):
    """ 设置采集代理服务器 """
    def __init__(self):
        self.proxies = webProxy.get_proxy_list()

    def process_request(self, request, spider):
        """ "http://127.0.0.1:8118" """
        proxys = choice(self.proxies)
        request.meta['proxy'] = "http://%s:%d" % (proxys.ip, proxys.port)


class SetUserAgentMiddleware(object):
    """ 设置userAgent """
    def __init__(self):
        self.user_agent = get_user_agent()

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.user_agent)
        request.headers.setdefault('Referer', 'http://www.baidu.com')


class SetHeaderMiddleware(object):
    """ 设置header协议 """
    def __init__(self):
        self.user_agent = get_user_agent()

    def process_request(self, request, spider):
        headers_list = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,und;q=0.2',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Transfer-Encoding': 'chunked',
            'Referer': 'http://www.baidu.com',
            'User-Agent': self.user_agent
        }
        for key, value in headers_list.items():
            request.headers.setdefault(key, value)


class IngoreHttpRequestMiddleware(object):
    """ 从下载器处开始拦截/过滤URL """
    def process_response(self, request, response, spider):
        if confRedis.exists('url:%s' % response.url):
            raise IgnoreRequest("IgnoreRequest : %s" % response.url)
        else:
            # Redis.set('url:%s' % response.url, 1)
            return response


class SetUtf8Middleware(object):
    """A downloader middleware to force utf8 encoding for all responses."""

    def process_response(self, request, response, spider):
        reload(sys)
        sys.setdefaultencoding("GBK")
        ubody = response.body_as_unicode().encode('GBK')
        # if isinstance(response, XmlResponse):
        #     ubody = response.body_as_unicode().encode('utf8')
        # elif gz.is_gzipped(response):
        #     ubody = gz.gunzip(response.body_as_unicode().encode('utf8'))
        # else:
        #     ubody = response.body_as_unicode().encode('utf8')
        #     logging.warning("Ignoring non-XML sitemap: %s" % response)
        return response.replace(body=ubody, encoding='GBK')

