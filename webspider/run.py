# python
# -*- coding: utf-8 -*-
from conf.config import DBSession, log_format, log_file, log_path, log_open, img_save_path
from model.Rule import Rule
from spiders.RuleSpider import RuleSpider

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
import logging
from datetime import datetime
import os


db = DBSession()


def run_spider():
    settings = Settings()
    settings.set("COOKIES_ENABLES", False)  # 禁止cookies追踪
    settings.set("ITEM_PIPELINES", {
        'pipelines.ImgPipline': 150,  # 保存图片到本地
        # 'pipelines.CoverImagesPipeline': 150, # 保存图片到七牛云
        'pipelines.SaveCommonPipline': 200,  # 保存数据库
        # 'pipelines.FilterUrlPipline': 300,
    })

    settings.set("DOWNLOADER_MIDDLEWARES", {
        'downloaderMiddlewareSet.IngoreHttpRequestMiddleware': 1,  # redis去重
        # 'downloaderMiddlewareSet.CountDropMiddleware': 2,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 自动useragent
        # 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,  # header头很容易造成读取失败,不建议开启
        # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        'downloaderMiddlewareSet.SetUserAgentMiddleware': 400,  # 设置useragent
        # 'downloaderMiddlewareSet.SetHeaderMiddleware': 550,
        'downloaderMiddlewareSet.SetProxyMiddleware': 750,  # 设置代理
        # 'downloaderMiddlewareSet.SetUtf8Middleware': 1000,  # 最开始设置字符集过滤用的,不用开启
    })

    settings.set("LOG_STDOUT ", False)
    # settings.set("CONCURRENT_REQUESTS", 20)
    settings.set("COOKIES_ENABLED", False)  # cookies追踪,采集新闻站可以关闭
    settings.set("RETRY_ENABLED", False)  # 设置重试,如果开启默认重试3次
    settings.set("REDIRECT_ENABLED", False)  # 重定向类网站是否采集
    # settings.set("AJAXCRAWL_ENABLED", True)
    settings.set("DOWNLOAD_DELAY", 3)  # 延迟下载
    settings.set("DOWNLOAD_TIMEOUT", 15)  # 下载超时的阈值,超过15秒就关闭连接

    # 图片处理
    # settings.set("IMAGES_STORE", "http://qiniu")  # 七牛云图片
    settings.set("IMAGES_STORE", img_save_path)  # 图片下载路径配置
    # settings.set("IMAGES_MIN_HEIGHT", "80")  # 图片最小高度 小于则不下载
    # settings.set("IMAGES_MIN_WIDTH", "80")  # 图片最小宽度 小于则不下载

    settings.set("TELNETCONSOLE_ENABLED", False)
    # 配置日志记录规则设置
    configure_logging(install_root_handler=False)
    # configure_logging()
    # 初始化日志路径

    if log_open is True:
        settings.set("LOG_LEVEL", 'INFO')
        logpath = datetime.now().strftime(log_path)
        if not os.path.isdir(logpath):
            os.makedirs(logpath)
        logging.basicConfig(
            filename=datetime.now().strftime('%s/%s_spider.log' % (logpath, log_file)),
            format=log_format,
            level=logging.INFO
        )

    # 拼装爬虫
    process = CrawlerProcess(settings)
    # 简单的过滤规则 支持sql 可以参看sql demo
    # 新增数据
    # sql = text('insert into users (u_name, u_password) values (:name, :password)')
    # data = db.execute(sql, {'name': 'nate1', 'password': password})
    # 删除数据
    # sql = text('delete from users where u_id = :id')
    #     data = session.execute(sql, {'id': last_id})
    # sql = text('select * from users')
    #    data = session.execute(sql)
    rules = db.query(Rule).filter(Rule.enable > 0).all()

    for rule in rules:
        process.crawl(RuleSpider, rule)
    process.start()

if __name__ == '__main__':
    run_spider()
