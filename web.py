#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import abort
from flask import render_template
from flask import request
from webspider.SearchApi import search
from webspider.conf.config import DBSession
from webspider.model.Classify import Classify

db = DBSession()

app = Flask(__name__)


# @app.route('/')
# def page_list():
#     pageList = db.query(Page).all()
#     page = pageList[0]
#     title = page.title.decode("GBK")
#     return render_template('search_list.html', title=title)
#
# app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    # abort(404)
    results = None
    keywords = None
    return render_template('index.html', results=results, keywords=keywords)


@app.route('/charts')
def charts():
    return render_template('charts.html')


@app.route('/tables')
def tables():
    return render_template('tables.html')


@app.route('/forms')
def forms():
    return render_template('forms.html')


@app.route('/test')
def tests():
    list = db.query(Classify).all()
    return render_template('test.html', list=list)


@app.route("/editc")
def editClass():
    return 1


@app.route("/delc")
def delClass():
    return 1


@app.route('/search')
@app.route('/search/')
@app.route('/search/<keywords>')
@app.route('/search/<keywords>/page/<page>')
def act_search(keywords="", page=1):
    if request.args:
        page = request.args['p'] if request.args['p'] else 1
    else:
        page = 1
    if not keywords:
        keywords = ""
        results = []
        print(1)
    else:
        keywords = unicode(keywords)
        results = search(keywords, int(page))
    return render_template('list.html', results=results, keywords=keywords)
    #     keywords = unicode(keywords)
    #     results = search(keywords, int(page))
    # return render_template('list.html', results=results, keywords=keywords)


# @app.route('/list')
# def page_list():
#     pageList = db.query(Page).all()
#     page = pageList[0]
#     return render_template('search_list.html', page=page)


if __name__ == '__main__':
    app.run(debug=True)
