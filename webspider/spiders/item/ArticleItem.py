# python
# -*- coding: utf-8 -*-
import scrapy


class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    html_title = scrapy.Field()
    html_body = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    publish_time = scrapy.Field()
    source_site = scrapy.Field()
    img_urls = scrapy.Field()
    thumb = scrapy.Field()
    img_list = scrapy.Field()
