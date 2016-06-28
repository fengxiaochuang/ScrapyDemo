# python
# -*- coding: utf-8 -*-
# import MySQLdb.cursors
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 初始化数据库连接:
engine = create_engine('mysql+mysqldb://root:root@127.0.0.1:3306/spider?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
confRedis = redis.StrictRedis(  # redis 服务器
    host='127.0.0.1',
    port=6379, db=4,
    password='pass123456'
)
check_proxy_url = "http://www.baidu.com"  # 默认的检查代理是否可用的链接

# base_path = "D:/PycharmProjects/webspider/"  # 项目部署的根目录
# img_base_path = "D:/PycharmProjects/webspider/"  # 项目图片保存的跟路径
img_save_path = "D:/PycharmProjects/webspider/image/"  # 图片保存的相对路径
# img_file = '%H'

log_open = True  # 是否开启日志记录
log_path = 'D:/PycharmProjects/webspider/webspider/log/%Y_%m_%d'  # 日志文件的保存路径 支持绝对路径 时间参数自动解析
log_file = '%H'  # 日志文件保存格式
log_format = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"  # 日志记录存储格式

html_path = 'D:/PycharmProjects/webspider/webspider/html'  # 采集到的html保存路径 支持绝对路径

# 索引文件路径
search_path = 'D:/PycharmProjects/webspider/webspider/search_index'

# page 里面的flag的默认值
default_page_flag = 1

# Data Source=.;Initial Catalog=master;Integrated Security=True
# Server=192.168.18.196;Initial Catalog=GB123;User ID=admin;Password=123456789
# qiniu
qiniu_config = {
    'access_key': "*",
    'secret_key': "*",
    'bucket_name': "*",
    'domain': "*"
}
