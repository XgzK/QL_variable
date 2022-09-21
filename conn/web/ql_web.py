from flask import Flask, render_template, request

from conn.gheaders.log import rz
from conn.fo.poadd import ym_change, upgrade, library, to_stop

app = Flask(__name__)
app._static_folder = "./templates/"


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        books = request.values.getlist('books[]')
        ku = request.values.get('ku')
        k = ''
        if len(ku) > 6:
            k = library(ku)
        # 把表单传递给方法添加到conn.yml
        q = ym_change(books)
        s = q + k
        return render_template('index.html', res=s)
    return render_template('index.html')


@app.route('/log')
def log():
    lo = rz()
    if lo == -1:
        return "日志为空"
    return lo


@app.route("/gi", methods=['GET', 'POST'])
def gi():
    if request.method == 'POST':
        git = request.values.get('gi')
        upgrade(int(git))
    return render_template('index.html')


@app.route("/pare", methods=['GET'])
def pare():
    if request.method == 'GET':
        return render_template('index.html', res=to_stop())


def run_web():
    app.run(
        host='0.0.0.0',
        port=5008,
        debug=False
    )
