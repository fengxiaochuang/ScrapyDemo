# python
# -*- coding: utf-8 -*-
from scrapy import Item, Field


class ProxyItem(Item):
    ip = Field()
    port = Field()
