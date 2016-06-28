#! python
# -*- coding: utf-8 -*-
from pyquery import PyQuery as pyQuery
from scrapy.spiders import Spider

from item.ProxyItem import ProxyItem


class GetProxySpider(Spider):
    name = "get_proxy"
    allowed_domains = ["proxynova.com"]
    start_urls = (
        'http://www.proxynova.com/proxy-server-list/country-cn/',
        'http://www.proxynova.com/proxy-server-list/elite-proxies/',
        'http://www.proxynova.com/proxy-server-list/anonymous-proxies/'
    )

    def parse(self, response):
        sel = pyQuery(response.body)
        sites = sel('#tbl_proxy_list > tbody:eq(0) > tr')
        proxy = ProxyItem()
        for row in sites:
            dom = pyQuery(row)
            if dom('td center div'):
                continue
            else:
                ip = dom('td:eq(0) span').text()
                proxy["ip"] = ip.strip() if ip else ""
                port = dom('td:eq(1)').text()
                proxy["port"] = port.strip() if port else ""
                yield proxy

