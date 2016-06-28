# python
# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from conf.config import log_path, log_file, log_format
from spiders.ProxySpider import GetProxySpider


def run_spider():
    settings = Settings()
    settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
    settings.set("ITEM_PIPELINES", {
        'pipelines.FilterProxyPipline': 1,
        'pipelines.SaveProxyPipeline': 2
    })
    settings.set("LOG_STDOUT ", True)

    # 配置日志记录规则设置
    # configure_logging({
    #     'filename': datetime.now().strftime('%Y_%m_%d_%H_proxy.log'),
    #     'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
    #     'level': logging.INFO
    # })
    configure_logging(install_root_handler=False)
    # 初始化日志路径
    logpath = datetime.now().strftime(log_path)
    if not os.path.isdir(logpath):
        os.makedirs(logpath)
    logging.basicConfig(
        filename=datetime.now().strftime('%s/%s_proxy.log' % (logpath, log_file)),
        format=log_format,
        level=logging.INFO
    )
    process = CrawlerProcess(settings)
    process.crawl(GetProxySpider)
    process.start()

if __name__ == '__main__':
    run_spider()
