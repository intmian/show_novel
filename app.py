import base64
from random import sample

from flask import Flask, send_file, render_template
from models.novels import novel
from flask import request, jsonify
from json import dumps

app = Flask(__name__)


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
            return send_file("static\\novels\\%s\\%s\\%s" % (name, name, book),
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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/novels/recommend')
def novel_recommend():
    ns = sample(novel.novels, 4)
    re = []
    for n in ns:
        re.append((n, novel.get_novel(n).cover))
    return jsonify(re)


@app.route('/novel/<novel_>', methods=['GET'])
def show_detail(novel_):
    novel.add_rank(novel_)
    return render_template('detail.html', novel=novel_)


# @app.route('/debug/novel')
# def novel_debug():
#     return send_file("static\\html\\detail_debug.html")


if __name__ == '__main__':
    app.run()
