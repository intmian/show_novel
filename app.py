﻿# -*- coding: UTF-8 -*-
import base64
from random import sample

from flask import Flask, send_file, render_template
from modules.novels import novel
from flask import request, jsonify
from json import loads

app = Flask(__name__)


# 高性能接口们
@app.route('/api/novel/lot')
def get_lot_novel():
    cover = False
    nos = None
    args = request.args or None
    if args:
        if "mode" in args:
            if args["mode"] == "cover":
                cover = True
        data = args["data"]
        nos = loads(data)
    re = []
    for no in nos:
        try:
            if no in novel.novels:
                n = novel.get_novel(no)
                if cover:
                    re.append({
                        "name": no,
                        "cover": n.cover
                    })
                else:
                    re.append({
                        "name": no,
                        "describe": n.describe.split("\n"),
                        "cover": n.cover,
                        "books": n.books
                    })
        except:
            pass
    return jsonify(re)


@app.route('/api/novels/rank/lot')
def get_lot_rank():
    re = []
    nos = novel.novels_rank()
    for no in nos:
        try:
            if no[0] in novel.novels:
                n = novel.get_novel(no[0])
                re.append({
                    "name": no[0],
                    "click": no[1],
                    "describe": n.describe.split("\n"),
                })
        except:  # 有可能会出现爬虫中的空结果，批量接口必须注意
            pass
    return jsonify(re)


@app.route('/api/novels/search/lot/<name>', methods=['GET'])
def search_lot(name):
    re = []
    nl = len(name)
    novels = novel.novels
    for n in novels:
        if n.find(name) != -1:
            re.append({
                "name": n,
                "rate": round(nl / len(n), 2)
            })  # 压入匹配程度
    re.sort(key=lambda x: x["rate"], reverse=True)
    for r in re:
        try:
            if r["name"] in novel.novels:
                n = novel.get_novel(r["name"])
                r["describe"] = n.describe.split("\n")
        except:  # 有可能会出现爬虫中的空结果，批量接口必须注意
            pass
    return jsonify(re)


@app.route('/api/novels', methods=['GET'])
def get_book():
    args = request.args or None
    if not args:
        return jsonify(novel.novels)
    if "left" not in args or "right" not in args:
        return jsonify([]), 400
    left, right = int(args["left"]), int(args["right"])
    l = len(novel.novels)
    if right > l or left < 0:
        return jsonify([]), 406
    return jsonify(novel.novels[left:right + 1])


@app.route('/api/novel/<name>', methods=['GET'])
def get_novel(name):
    if name not in novel.novels:
        return jsonify(None), 404
    else:
        args = request.args or None
        if args:
            if "mode" in args:
                if args["mode"] == "cover":
                    n = novel.get_novel(name)
                    return n.cover
        n = novel.get_novel(name)
        return jsonify({
            "describe": n.describe.split("\n"),
            "cover": n.cover,
            "books": n.books
        })


@app.route('/api/novel/<name>/<book>', methods=['GET'])
def book_download(name, book):
    if name not in novel.novels:
        return jsonify(None), 404
    else:
        n = novel.get_novel(name)
        if book not in n.books:
            return jsonify(None), 404
        else:
            return send_file("static/novels/%s/%s/%s" % (name, name, book),
                             attachment_filename=name + "_" + book,
                             as_attachment=True)


@app.route('/api/novels/num', methods=['GET'])
def get_book_name():
    return jsonify(len(novel.novels))


@app.route('/api/novels/search/<name>', methods=['GET'])
def search(name):
    re = []
    nl = len(name)
    novels = novel.novels
    for n in novels:
        if n.find(name) != -1:
            re.append((n, round(nl / len(n), 2)))  # 压入匹配程度
    re.sort(key=lambda x: x[1], reverse=True)
    return jsonify(re)


@app.route('/api/novels/popular', methods=['GET'])
def popu():
    return jsonify(novel.novels_popular())


@app.route('/api/novels/rank', methods=['GET'])
def rank():
    return jsonify(novel.novels_rank())


@app.route('/api/novels/recommend')
def novel_recommend():
    ns = sample(novel.novels, 4)
    re = []
    for n in ns:
        re.append((n, novel.get_novel(n).cover))
    return jsonify(re)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/novel/<novel_>', methods=['GET'])
def show_detail(novel_):
    novel.add_rank(novel_)
    return render_template('detail.html', novel=novel_)


@app.route('/search/<word>', methods=['GET'])
def search_novel(word):
    return render_template('search.html', word=word)


@app.route('/rank', methods=['GET'])
def rank_novel():
    return render_template('rank.html')


# @app.route('/debug/novel')
# def novel_debug():
#     return send_file("static\\html\\detail_debug.html")

# @app.route('/debug/novels')
# def novel_debug():
#     return send_file("static\\html\\index_debug.html")
@app.route('/debug/search')
def novel_debug():
    return send_file("static\\html\\search_debug.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
