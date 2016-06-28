# -*- coding: utf-8 -*-
from scrapy import Item, Field


class ImgItem(Item):
    img_urls = Field()
    images = Field()
    image_paths = Field()
    or_url = Field()
    body = Field()
    first_img = Field()
