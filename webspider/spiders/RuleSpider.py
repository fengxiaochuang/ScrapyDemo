# python
# -*- coding: utf-8 -*-
import sys
import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from item.ArticleItem import ArticleItem as Article
import re


class RuleSpider(CrawlSpider):
    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.weburl_id = rule.weburl_id
        self.rule_id = rule.rule_id
        self.thumb_img_xpath = rule.thumb_img_xpath
        self.start_urls = rule.start_urls.split(",")
        rule_list = []
        if rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page)))
        rule_list.append(Rule(LinkExtractor(allow=[rule.allow_url], restrict_xpaths=[rule.extract_from]),
                              callback='parse_item'))
        self.rules = tuple(rule_list)
        super(RuleSpider, self).__init__()

    def parse_item(self, response):
        reload(sys)
        sys.setdefaultencoding("GBK")
        article = Article()
        article["url"] = response.url
        # 本身的html标题
        html_title = response.xpath("//title/text()").extract()
        article["html_title"] = html_title[0] if html_title else ""
        article["html_body"] = response.body
        # 标题
        try:
            title = response.xpath(self.rule.title_xpath).extract()
            article["title"] = title[0] if title else ""
        except Exception:
            article["title"] = ""
        # 内容
        try:
            # html_filter = re.sub(response.xpath("//iframe"), "", response.body)
            body = response.xpath(self.rule.body_xpath).extract()
            # article["body"] = ""
            # for texts in len(body):
            #     article["body"] += re.sub(Selector(text=texts).xpath("//iframe"), "", texts)
            article["body"] = '\n'.join(body) if body else ""
        except Exception:
            article["body"] = ""
        # 发布时间
        try:
            publish_time = response.xpath(self.rule.publish_time_xpath).extract()
            article["publish_time"] = publish_time[0] if publish_time else ""
        except Exception:
            article["publish_time"] = ""
        # 来源
        try:
            source_site = response.xpath(self.rule.source_site_xpath).extract()
            article["source_site"] = source_site[0] if source_site else ""
        except Exception:
            article["source_site"] = ""

        # 图片
        image_urls = response.xpath(self.rule.body_xpath + "//img/@src").extract()
        # article["img_urls"]["original"] = []
        # article["img_urls"]["real"] = []
        article["img_urls"] = {"original": [], "real": []}
        if image_urls:
            for img in image_urls:
                article["img_urls"]["original"].append(img)
                article["img_urls"]["real"].append(urlparse.urljoin(response.url, img))
        else:
            article["img_urls"] = None
        article["thumb"] = ""
        if article["title"] == "" or article["body"] == "":
            return None
        else:
            return article
