# -*- coding: utf-8 -*-
import sys
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from item.ImgItem import ImgItem
import urlparse


class ImgSpider(CrawlSpider):
    name = 'imgspider'
    start_urls = ['http://news.163.com/15/1221/11/BBBS3IAG00014AED.html#f=dlist']
    # start_urls = ['http://www.cocloud.net/2013/09/10/scrapy_img_spider.html']
    image_names = {}

    def parse(self, response):
        item = ImgItem()
        # item['image_urls'] = response.xpath("//div[@class='container']//img/@src").extract()
        # item['img_urls'] = response.xpath("//div[@id='endText']//img/@src").extract()
        # for index, value in enumerate(item['image_urls']):
        #     number = self.start_urls.index(response.url) * len(item['image_urls']) + index
        #     self.image_names[value] = 'full/%04d.jpg' % number
        # image_urls = response.xpath(self.rule.body_xpath + "//img/@src").extract()
        body = response.xpath("//div[@id='endText']").extract()
        item['body'] = body[0]
        image_urls = response.xpath("//div[@id='endText']//img/@src").extract()
        # article["img_urls"]["original"] = []
        # article["img_urls"]["real"] = []
        item["img_urls"] = {"original": [], "real": []}
        if image_urls:
            for img in image_urls:
                item["img_urls"]["original"].append(img)
                item["img_urls"]["real"].append(urlparse.urljoin(response.url, img))
        else:
            item["img_urls"] = None
        yield item
