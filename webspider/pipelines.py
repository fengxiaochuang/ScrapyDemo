# coding:utf-8
import hashlib
import re
import time
from scrapy.exceptions import DropItem
from scrapy.http import Request, Response
from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
from sqlalchemy import exc
from QiniuStorage import Qiniu
from conf.config import DBSession, confRedis, html_path, qiniu_config, default_page_flag
from model.Page import Page
from model.Proxy import Proxy
from util import WebProxy as webProxy
from util import common as utils


# from model.Article import Article as Page


class FilterProxyPipline(object):
    """ 过滤不能用的代理 """

    def process_item(self, item, spider):
        ret = webProxy.check_proxy(item['ip'], item['port'])
        if ret:
            return item
        else:
            raise DropItem("Duplicate item found: %s:%s" % (item['ip'], item['port']))


class SaveProxyPipeline(object):
    """ 保存代理到数据库 """

    def process_item(self, item, spider):
        # try:
        #     con = MySQLdb.connect(**config.db_config)
        #     cur = con.cursor()
        #     sql = "INSERT INTO leiju_proxy (ip,port,proto,checked_at,created_at) VALUES (%s,%s,%s,%s,%s)"
        #     parmam = [(item['ip'], item['port'], 'http', int(time.time()), int(time.time()))]
        #     cur.executemany(sql, parmam)
        #     con.commit()
        #     con.close()
        #     # return item
        # except Exception, e:
        #     logging.info("SaveError: %s:%s %s" % (item['ip'], item['port'], format(e)))
        #     raise DropItem("SaveError: %s:%s %s" % (item['ip'], item['port'], format(e)))
        db = DBSession()
        md5 = hashlib.md5()
        md5.update(item['ip'] + "." + item['port'])
        haship = md5.hexdigest()
        proxy = Proxy(haship=haship, ip=item['ip'], port=item['port'], create_time=int(time.time()))
        db.add(proxy)
        try:
            db.commit()
        except exc.SQLAlchemyError, e:
            raise DropItem("SaveError: %s:%s %s" % (item['ip'], item['port'], format(e)))
        finally:
            db.close()


# class FilterUrlPipline(object):
#     """ use redis to fileter url """
#     def process_item(self, item, spider):
#         redis = confRedis
#         redis.set('url:%s' % item["url"], 1)
#         return item


class SaveCommonPipline(object):
    """ save common spider result to local """

    def process_item(self, item, spider):
        db = DBSession()
        redis = confRedis

        rule_id = spider.rule_id
        url = item['url']
        md5 = hashlib.md5()
        md5.update(url)
        urlmd5 = md5.hexdigest()
        site_name = utils.get_site(item['url'])
        # site_name = spider.rule['allow_domains']
        html_title = item['html_title']
        # html_body = item['html_body']
        save_path = utils.md5dir(item['url'])
        save_time = int(time.time())
        title = item['title'] if 'title' in item else ""
        body = item['body'] if 'body' in item else ""
        thumb = item['thumb'] if 'thumb' in item else ""
        img_list = item['img_list'] if 'img_list' in item else ""

        # TODO 这里使用一个分析方法,分析抓取到数据的发布时间,然后转换成时间戳
        publish_time = utils.smart2date(item['publish_time']) if 'publish_time' in item else ""
        source_site = item['source_site'] if 'source_site' in item else ""
        flag = default_page_flag

        page = Page(rule_id=rule_id, url=item['url'], urlmd5=urlmd5, site_name=site_name, html_title=html_title,
                    save_path=save_path,
                    save_time=save_time, title=title,
                    thumb=thumb, img_list=img_list,
                    body=body, publish_time=publish_time,
                    source_site=source_site, flag=flag)
        has = db.query(Page).filter(Page.urlmd5 == urlmd5).first()
        if has:
            page = Page(rule_id=rule_id, url=item['url'], site_name=site_name, html_title=html_title,
                        save_path=save_path,
                        save_time=save_time, title=title,
                        thumb=thumb, img_list=img_list,
                        body=body, publish_time=publish_time,
                        source_site=source_site, flag=flag)

        db.add(page)
        try:
            db.commit()
            utils.save_file('%s/%s' % (html_path, save_path), item['html_body'])
            redis.set('url:%s' % url, 1)
        except exc.SQLAlchemyError, e:
            raise DropItem("SaveDbError: %s,%s" % (url, format(e)))


class ImgPipline(ImagesPipeline):
    """ 普通图片下载 """

    def file_path(self, request, response=None, info=None):
        # image_name = ImgSpider.image_names[request.url]
        # return image_name
        image_guid = hashlib.sha1(request.url).hexdigest()
        part1 = image_guid[0:2]
        # part2 = md5url[2:4]
        # part3 = md5url[4:6]
        # filepath = "%s/%s/%s/%s/%s/%s.html" % (datestr, site.hostname, part1, part2, part3, md5url)
        filepath = "%s/%s.jpg" % (part1, image_guid)
        # return 'full/%s' % image_guid
        return filepath

    def get_media_requests(self, item, info):
        if item['img_urls']:
            for image_url in item['img_urls']['real']:
                yield Request(image_url)

    def item_completed(self, results, item, info):
        i = 0
        image_paths = []
        for ok, x in results:
            if ok:
                # TODO 正则替换items里面的img
                item["body"] = re.sub(item['img_urls']["original"][i], x["path"], item["body"])
                image_paths.append(x['path'])
            i += 1
        # item['or_url'] = or_url
        item["thumb"] = image_paths[0] if image_paths else ""
        item["img_list"] = ','.join(image_paths) if image_paths else ""
        return item


class CoverImagesPipeline(ImagesPipeline):
    """ 七牛云存储图片上传 """
    ImagesPipeline.STORE_SCHEMES['http'] = Qiniu
    URL_PREFIX = None

    @classmethod
    def from_settings(cls, settings):
        # cls.MIN_WIDTH = settings.getint('IMAGES_MIN_WIDTH', 0)
        # cls.MIN_HEIGHT = settings.getint('IMAGES_MIN_HEIGHT', 0)
        # cls.EXPIRES = settings.getint('IMAGES_EXPIRES', 90)
        # cls.THUMBS = settings.get('IMAGES_THUMBS', {})
        qiniu = cls.STORE_SCHEMES['http']
        return super(CoverImagesPipeline, cls).from_settings(settings)

    def get_media_requests(self, item, info):
        if item['img_urls']:
            for image_url in item['img_urls']['real']:
                yield Request(image_url)

    def item_completed(self, results, item, info):
        i = 0
        image_paths = []
        for ok, x in results:
            if ok:
                # TODO 正则替换items里面的img
                tmp_path = qiniu_config["domain"] + x["path"]
                item["body"] = re.sub(item['img_urls']["original"][i], tmp_path, item["body"])
                image_paths.append(tmp_path)
            i += 1
        item["thumb"] = image_paths[0] if image_paths else ""
        return item
