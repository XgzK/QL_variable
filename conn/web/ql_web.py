from flask import Flask, render_template, request

from conn.gheaders.log import rz
from conn.fo.poadd import ym_change, upgrade

app = Flask(__name__)
app._static_folder = "./templates/"


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        books = request.values.getlist('books[]')
        # 把表单传递给方法添加到conn.yml
        return render_template('index.html', res=ym_change(books))
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


def run_web():
    app.run(
        host='0.0.0.0',
        port=5008,
        debug=False
    )
