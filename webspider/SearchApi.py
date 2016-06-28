# python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
from conf.config import search_path
# from jieba.analyse import ChineseAnalyzer
from whoosh import scoring, sorting
from whoosh.query import *
import HTMLParser


# sys.path.append("../")


# analyzer = ChineseAnalyzer()


def search(inputstring="", page=1, size=10):
    """
    搜索接口
    :type inputstring: 传入搜索字符串
    :param page: 页数
    :param size: 每页显示的多少
    """
    inputstring = unicode(inputstring)
    res = []
    results = []
    # if __name__ == '__main__':
    #     index_path = "./sindex"
    # else:
    #     index_path = "./webspider/sindex"
    index_path = search_path
    try:
        ix = open_dir(index_path)  # 搜索路径
    except Exception, e:
        pass
    else:
        if not inputstring:
            pass
        else:
            publish_time = sorting.FieldFacet("publish_time", reverse=True)
            qp = MultifieldParser(["title", "body"], schema=ix.schema)
            with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
                querystring = qp.parse(inputstring)
                results = searcher.search(querystring, terms=True, limit=None, sortedby=[publish_time])
                # print(len(results))
                # results = searcher.search_page(querystring, page)
                html_parser = HTMLParser.HTMLParser()
                if len(results) > 0:
                    for i in xrange((page - 1) * size, page * size):
                        if i in xrange(len(results)):
                            tmpret = results[i].fields()
                            hit_keywords = set()
                            for key, val in results[i].matched_terms():
                                hit_keywords.add(val.decode('utf-8'))
                                # hit_keywords.add(val.encode('latin1').decode('gbk'))
                            tmpret['words'] = results[i].matched_terms()
                            tmpret['hit_keywords'] = " ".join(list(hit_keywords))
                            tmpret['hit_title'] = html_parser.unescape(results[i].highlights('title')) if results[i].highlights('title') else results[i]['title']
                            # tmpret['hit_title'] = html_parser.\
                            #     unescape(results[i].highlights('title').encode('latin1')).decode('unicode_escape') \
                            #     if results[i].highlights('title') else results[i]['title']

                            # print html_parser.unescape(results[i].highlights('title').encode('utf-8'))
                            # tmpret['hit_body'] = results[i].highlights('body')
                            res.append(tmpret)

    page_info = {'total': len(results), 'page': page, 'size': size, 'data': res}
    return page_info


if __name__ == '__main__':
    ret = search("中国")
    print(ret)
    #
    # ix = open_dir("./sindex")  # for read only
    # searcher = ix.searcher()
    # parser = QueryParser("body", schema=ix.schema)
    # q = parser.parse(u"中国")
    # results = searcher.search(q)
    # for hit in results:
    #     print(hit)
    #     print("=" * 10)
