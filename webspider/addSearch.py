# python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
import datetime
from whoosh.index import create_in
from whoosh.fields import *
from conf.config import DBSession, search_path
from model.Page import Page
from sqlalchemy import text

from jieba.analyse import ChineseAnalyzer
analyzer = ChineseAnalyzer()
# sys.path.append("../")

schema = Schema(
    page_id=NUMERIC(),
    title=TEXT(stored=True, analyzer=analyzer),
    body=TEXT(stored=True, analyzer=analyzer),
    url=ID(stored=True),
    # site_name=ID(stored=True),
    # html_title=TEXT(stored=True),
    # source_site=ID(stored=True),
    publish_time=DATETIME(stored=True),
    save_time=DATETIME(stored=True),
    # save_path=TEXT(stored=True)
)
if not os.path.exists(search_path):
    os.mkdir(search_path)

ix = create_in(search_path, schema)
writer = ix.writer()
# fromtimestamp int->time
# time = 0
# datetime.datetime.fromtimestamp(time)
# strptime string->time
# format = '%Y-%m-%d %H:%M:%S' str = '2015-10-27 15:09:38'
# datetime.datetime.strptime(str,format)

timeformat = '%Y-%m-%d %H:%M:%S'
db = DBSession()
""" 过滤条件参照该文件最下面的增量索引的方案 """
# 新增数据
# sql = text('insert into users (u_name, u_password) values (:name, :password)')
# data = db.execute(sql, {'name': 'nate1', 'password': password})
# 删除数据
# sql = text('delete from users where u_id = :id')
#     data = session.execute(sql, {'id': last_id})
# sql = text('select * from users')
#    data = session.execute(sql)

# 查询SQL版本
sql = text('select * from Page where id < :id')
pageList = db.execute(sql, {'id': 20})
# 查询ORM版本
# pageList = db.query(Page).filter(Page.id < 20).all()

i = 0
for row in pageList:
    publish_time = datetime.datetime.strptime(row.publish_time, timeformat)
    save_time = datetime.datetime.fromtimestamp(row.save_time)
    # print(type(row.title))
    writer.add_document(
        page_id=row.id,
        title=row.title,
        body=row.body,
        url=row.url,
        # site_name=row.site_name,
        # html_title=row.html_title,
        # source_site=row.source_site,
        publish_time=publish_time,
        save_time=save_time,
        # save_path=row.save_path
    )
    i += 1
    print("inserting the %s rows" % i)\
# 可以在循环内部提交
db.close()
writer.commit()
print("all had inserted!!!")
"""
使用标志位的办法增量添加.
1. 标志位为0的是待添加对象,
2. 标志位为1是已经添加的对象.
3. 这里可以设置一个添加的日志文件.
4. 上传完成之后修改数据库和生成日志文件.
5. 日志文件只用简单的串行化page_id存储即可.
"""
