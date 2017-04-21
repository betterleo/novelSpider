from flask import Flask
from front import *
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    res = front().get_novel_list_for_index()
    return render_template("index.html", data=res)


@app.route('/book/<novel_id>')
def chapter_list(novel_id):
    res = front().get_novel_object(novel_id)
    return render_template("novel.html", data=res)


@app.route('/book/<novel_id>/<chapter_id>')
def chapter(novel_id, chapter_id):
    res = front().get_chapter_detail(novel_id, chapter_id)
    return render_template("chapter.html", data=res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080',threaded=True)
